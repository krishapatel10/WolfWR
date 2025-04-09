from db.connection import create_connection, close_connection

def transfer_product(self, source_store_id, dest_store_id, product_id, transfer_quantity):
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor()
        conn.start_transaction()  # Start a transaction

        # Check if product exists in destination store
        cursor.execute("""
            SELECT ProductID FROM Inventory WHERE StoreID = %s AND ProductID = %s
        """, (dest_store_id, product_id))
        result = cursor.fetchone()

        # If the product doesn't exist in destination store, add it
        if not result:
            cursor.execute("""
                INSERT INTO Inventory (StockQuantity, StoreID, ProductID)
                SELECT StockQuantity, %s, ProductID 
                FROM Products WHERE ProductID = %s
            """, (dest_store_id, product_id))

        # Deduct stock from source store
        cursor.execute("""
            UPDATE Inventory SET StockQuantity = StockQuantity - %s 
            WHERE ProductID = %s AND StoreID = %s
        """, (transfer_quantity, product_id, source_store_id))

        # Add stock to destination store
        cursor.execute("""
            UPDATE Inventory SET StockQuantity = StockQuantity + %s
            WHERE ProductID = %s AND StoreID = %s
        """, (transfer_quantity, product_id, dest_store_id))

        conn.commit()  # COMMIT if all operations succeed
        print("Product transferred successfully.")

    except Exception as e:
        print(f"Error occurred while transferring product: {e}")
        conn.rollback()  # ROLLBACK on failure
    finally:
        cursor.close()
        close_connection(conn)
