from db.connection import create_connection, close_connection

def add_product(ProductID, Name, StockQuantity, BuyPrice, MarketPrice, ExpirationDate, SupplierID, ProductionDate, StoreID):
    conn = create_connection()
    if not conn:
        print("❌ Could not connect to DB.")
        return

    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO Product (ProductID, Name, StockQuantity, BuyPrice, MarketPrice, ExpirationDate, SupplierID, ProductionDate, StoreID)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (ProductID, Name, StockQuantity, BuyPrice, MarketPrice, ExpirationDate, SupplierID, ProductionDate, StoreID))
        conn.commit()
        print("✅ Product added successfully.")
    except Exception as e:
        conn.rollback()
        print("❌ Error adding product:", e)
    finally:
        cursor.close()
        close_connection(conn)

def update_product(ProductID, Name=None, StockQuantity=None, BuyPrice=None, MarketPrice=None, ExpirationDate=None, SupplierID=None, ProductionDate=None, StoreID=None):
    conn = create_connection()
    if not conn:
        print("❌ Could not connect to DB.")
        return

    try:
        cursor = conn.cursor()
        fields = []
        values = []

        if Name is not None:
            fields.append("Name = %s")
            values.append(Name)
        if StockQuantity is not None:
            fields.append("StockQuantity = %s")
            values.append(StockQuantity)
        if BuyPrice is not None:
            fields.append("BuyPrice = %s")
            values.append(BuyPrice)
        if MarketPrice is not None:
            fields.append("MarketPrice = %s")
            values.append(MarketPrice)
        if ExpirationDate is not None:
            fields.append("ExpirationDate = %s")
            values.append(ExpirationDate)
        if SupplierID is not None:
            fields.append("SupplierID = %s")
            values.append(SupplierID)
        if ProductionDate is not None:
            fields.append("ProductionDate = %s")
            values.append(ProductionDate)
        if StoreID is not None:
            fields.append("StoreID = %s")
            values.append(StoreID)

        if not fields:
            print("⚠️ Nothing to update.")
            return

        query = f"UPDATE Product SET {', '.join(fields)} WHERE ProductID = %s"
        values.append(ProductID)

        cursor.execute(query, tuple(values))
        conn.commit()
        print("✅ Product updated successfully.")
    except Exception as e:
        conn.rollback()
        print("❌ Error updating product:", e)
    finally:
        cursor.close()
        close_connection(conn)

def delete_product(ProductID):
    conn = create_connection()
    if not conn:
        print("❌ Could not connect to DB.")
        return

    try:
        cursor = conn.cursor()
        query = "DELETE FROM Product WHERE ProductID = %s"
        cursor.execute(query, (ProductID,))
        conn.commit()
        print("✅ Product deleted successfully.")
    except Exception as e:
        conn.rollback()
        print("❌ Error deleting product:", e)
    finally:
        cursor.close()
        close_connection(conn)
