from db.connection import create_connection, close_connection

def generate_bills_for_supplier(self, supplier_id):
    # Create a cursor object to execute queries
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor(dictionary=True)
        # Define the query to retrieve bills for the given supplier
        query = """
            SELECT s.SupplierID, s.Name, SUM(b.Amount) AS TotalAmount
            FROM Suppliers s
            JOIN Billing b ON s.SupplierID = b.SupplierID
            WHERE s.SupplierID = %s
            GROUP BY s.SupplierID, s.Name;
        """
        
        # Execute the query
        cursor.execute(query, (supplier_id,))

        # Fetch the result
        result = cursor.fetchone()

        # Check if a result is returned
        if result:
            supplier_id, supplier_name, total_amount = result
            print(f"Bill Summary for Supplier ID {supplier_id} ({supplier_name}):")
            print(f"Total Amount: ${total_amount:.2f}")
        else:
            print(f"No bills found for Supplier ID {supplier_id}.")
    
    except Exception as e:
        print(f"Error generating bill summary for Supplier ID {supplier_id}: {str(e)}")
    
    finally:
        cursor.close()
        close_connection(conn)
