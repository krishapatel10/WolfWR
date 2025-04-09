from db.connection import create_connection, close_connection

# Add a new inventory record
def add_inventory(InventoryID, StockQuantity, StoreID, ProductID, LastStockUpdate):
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO Inventory (InventoryID, StockQuantity, StoreID, ProductID, LastStockUpdate)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (InventoryID, StockQuantity, StoreID, ProductID, LastStockUpdate))
        conn.commit()
        print(f"Inventory {InventoryID} added successfully.")
    except Exception as e:
        conn.rollback()
        print("Error adding inventory:", e)
    finally:
        cursor.close()
        close_connection(conn)

# Update an existing inventory record
def update_inventory(InventoryID, StockQuantity, StoreID, ProductID, LastStockUpdate):
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor()
        query = """
        UPDATE Inventory
        SET StockQuantity = %s, StoreID = %s, ProductID = %s, LastStockUpdate = %s
        WHERE InventoryID = %s
        """
        cursor.execute(query, (StockQuantity, StoreID, ProductID, LastStockUpdate, InventoryID))
        conn.commit()
        print(f"Inventory {InventoryID} updated successfully.")
    except Exception as e:
        conn.rollback()
        print("Error updating inventory:", e)
    finally:
        cursor.close()
        close_connection(conn)

# Delete an inventory record
def delete_inventory(InventoryID):
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor()
        query = """
        DELETE FROM Inventory WHERE InventoryID = %s
        """
        cursor.execute(query, (InventoryID,))
        conn.commit()
        print(f"Inventory {InventoryID} deleted successfully.")
    except Exception as e:
        conn.rollback()
        print("Error deleting inventory:", e)
    finally:
        cursor.close()
        close_connection(conn)
