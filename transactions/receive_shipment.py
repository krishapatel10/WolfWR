from db.connection import create_connection, close_connection
from datetime import datetime

def recieve_shipment(product_id, supplier_id, store_id, quantity_received, amount, billing_staff_id):
    """
    Adds a new shipment to the system, updates inventory, and updates the billing record.
    """
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor()

        # Step 1: Insert the shipment record into the Shipments table
        shipment_date = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("""
            INSERT INTO Shipments (ProductID, SupplierID, StoreID, QuantityReceived, DateReceived)
            VALUES (%s, %s, %s, %s, %s);
        """, (product_id, supplier_id, store_id, quantity_received, shipment_date))

        # Step 2: Update the Billing table to add the cost of the received shipment
        cursor.execute("""
            INSERT INTO Billing (BillingStaffID, StoreID, SupplierID, Amount, DueDate, PaidStatus)
            VALUES (%s, %s, %s, %s, DATE_ADD(CURDATE(), INTERVAL 30 DAY), 0);
        """, (billing_staff_id, store_id, supplier_id, amount))

        # Commit the transaction
        conn.commit()
        print(f"Shipment added successfully for ProductID {product_id} in StoreID {store_id}.")
        
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        conn.rollback()
    finally:
        cursor.close()
        close_connection(conn)
