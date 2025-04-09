from db.connection import create_connection, close_connection
from datetime import datetime

def calculate_total_price_with_discount(transaction_id):
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        
        # Get all items for the transaction
        cursor.execute("""
            SELECT ti.ProductID, ti.Quantity, ti.UnitPrice
            FROM TransactionItems ti
            WHERE ti.TransactionID = %s
        """, (transaction_id,))
        items = cursor.fetchall()
        
        if not items:
            print(f"No items found for transaction {transaction_id}")
            return 0.0
        
        # Get the purchase date for the transaction
        cursor.execute("""
            SELECT PurchaseDate FROM Transactions WHERE TransactionID = %s
        """, (transaction_id,))
        transaction = cursor.fetchone()
        if not transaction:
            print(f"Transaction {transaction_id} not found")
            return 0.0
        
        purchase_date = transaction['PurchaseDate']
        
        total_price = 0.0
        
        # Calculate price for each item with applicable discounts
        for item in items:
            product_id = item['ProductID']
            quantity = item['Quantity']
            unit_price = item['UnitPrice']
            
            # Check for active discounts for this product on the purchase date
            cursor.execute("""
                SELECT DiscountRate 
                FROM Discounts 
                WHERE ProductID = %s 
                AND %s BETWEEN ValidFrom AND ValidTo
            """, (product_id, purchase_date))
            
            discount = cursor.fetchone()
            discount_rate = discount['DiscountRate'] if discount else 0.0
            
            # Calculate discounted price for this item
            discounted_price = unit_price * (1 - discount_rate / 100)
            item_total = discounted_price * quantity
            
            total_price += item_total
            
        return round(total_price, 2)
        
    except Exception as e:
        print("Error calculating total price with discount:", e)
        return None
        
    finally:
        cursor.close()
        close_connection(conn)

# Example usage:
if __name__ == "__main__":
    # Test with transaction 704 which has a product (306) that had a discount
    # but only between 2024-04-10 and 2024-05-10
    # The purchase date is 2024-07-23, so discount shouldn't apply
    transaction_id = 704
    total = calculate_total_price_with_discount(transaction_id)
    print(f"Total price for transaction {transaction_id} with discounts: ${total if total is not None else 'Error'}")
    
    # Test with transaction 702 which has no products with active discounts
    transaction_id = 702
    total = calculate_total_price_with_discount(transaction_id)
    print(f"Total price for transaction {transaction_id} with discounts: ${total if total is not None else 'Error'}")

def update_store_info(StoreID, Address=None, Phone=None, ManagerID=None):
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor()
        fields = []
        values = []

        if Address is not None:
            fields.append("Address = %s")
            values.append(Address)
        if Phone is not None:
            fields.append("Phone = %s")
            values.append(Phone)
        if ManagerID is not None:
            fields.append("ManagerID = %s")
            values.append(ManagerID)

        if not fields:
            print("Nothing to update.")
            return

        query = f"UPDATE Stores SET {', '.join(fields)} WHERE StoreID = %s"
        values.append(StoreID)
        cursor.execute(query, tuple(values))
        conn.commit()
        print("Store updated successfully.")

    except Exception as e:
        conn.rollback()
        print("Error updating store:", e)

    finally:
        cursor.close()
        close_connection(conn)

def delete_store_info(StoreID):
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor()
        query = "DELETE FROM Stores WHERE StoreID = %s"
        cursor.execute(query, (StoreID,))
        conn.commit()
        print("Store deleted successfully.")
    except Exception as e:
        conn.rollback()
        print("Error deleting store:", e)
    finally:
        cursor.close()
        close_connection(conn)
