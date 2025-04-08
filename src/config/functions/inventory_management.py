from utils.db_conn import get_connection
from datetime import date


class InventoryManager:
    
    def insert_inventory_record(inventory_id, stock_quantity, store_id, product_id):
            conn = get_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO Inventory (InventoryID, StockQuantity, StoreID, ProductID) VALUES (%s, %s, %s, %s)",
                        (inventory_id, stock_quantity, store_id, product_id)
                    )
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                conn.close()

    def update_inventory_record(product_id, store_id, quantity_change):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE Inventory SET StockQuantity = StockQuantity + %s WHERE ProductID = %s AND StoreID = %s",
                    (quantity_change, product_id, store_id)
                )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def view_updated_inventory(product_id, store_id):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM Inventory WHERE ProductID = %s AND StoreID = %s",
                    (product_id, store_id)
                )
                inventory = cursor.fetchall()
            return inventory
        finally:
            conn.close()


    def transfer_inventory(product_id, source_store_id, destination_store_id, quantity):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                # Deduct from source store
                cursor.execute(
                    "UPDATE Inventory SET StockQuantity = StockQuantity - %s WHERE ProductID = %s AND StoreID = %s",
                    (quantity, product_id, source_store_id)
                )
                
                # Add to destination store
                cursor.execute(
                    "UPDATE Inventory SET StockQuantity = StockQuantity + %s WHERE ProductID = %s AND StoreID = %s",
                    (quantity, product_id, destination_store_id)
                )
            
            # Commit both changes as a single transaction
            conn.commit()
            
        except Exception as e:
            conn.rollback()  # Rollback the transaction if an error occurs
            raise e
        finally:
            conn.close()


    def check_missing_products_in_inventory():
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT Products.ProductID 
                    FROM Products 
                    LEFT JOIN Inventory ON Inventory.ProductID = Products.ProductID 
                    WHERE Inventory.ProductID IS NULL;
                """)
                missing_products = cursor.fetchall()
            return missing_products
        finally:
            conn.close()

    def add_product(product_id, name, stock_quantity, buy_price, market_price, supplier_id):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Products (ProductID, Name, StockQuantity, BuyPrice, MarketPrice, SupplierID) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (product_id, name, stock_quantity, buy_price, market_price, supplier_id)
                )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()


    def add_missing_products_to_inventory(store_id):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                # Insert missing products into inventory
                cursor.execute("""
                    INSERT INTO Inventory (StockQuantity, StoreID, ProductID)
                    SELECT Products.StockQuantity, %s, Products.ProductID
                    FROM Products
                    LEFT JOIN Inventory ON Inventory.ProductID = Products.ProductID
                    WHERE Inventory.ProductID IS NULL
                """, (store_id,))
            
            # Commit the changes
            conn.commit()
            
        except Exception as e:
            conn.rollback()  # Rollback the transaction if an error occurs
            raise e
        finally:
            conn.close()


    def generate_bills_for_supplier(supplier_id):
        conn = get_connection()
        if conn is None:
            print("Database connection failed!")
            return
        
        try:
            with conn.cursor(dictionary=True) as cursor:
                query = """
                    SELECT 
                        s.SupplierID, 
                        s.Name, 
                        SUM(b.Amount) AS TotalAmount 
                    FROM 
                        Suppliers s
                    JOIN 
                        Billing b ON s.SupplierID = b.SupplierID
                    WHERE 
                        s.SupplierID = %s 
                    GROUP BY 
                        s.SupplierID, s.Name;
                """
                cursor.execute(query, (supplier_id,))
                result = cursor.fetchall()
                
                if result:
                    for row in result:
                        print(f"Supplier: {row['Name']}, Total Billing Amount: {row['TotalAmount']}")
                else:
                    print("No records found for the supplier.")
        except Error as e:
            print(f"Error while executing the query: {e}")
        finally:
            conn.close()

    def generate_reward_checks_for_platinum_customers():
        conn = get_connection()
        if conn is None:
            print("Database connection failed!")
            return
        
        try:
            with conn.cursor(dictionary=True) as cursor:
                query = """
                    SELECT 
                        c.CustomerID, 
                        c.Name, 
                        COALESCE(SUM(r.RewardAmount), 0) AS RewardCheck
                    FROM 
                        Customers c
                    JOIN 
                        Transactions t ON c.CustomerID = t.CustomerID
                    JOIN 
                        Memberships m ON c.CustomerID = m.CustomerID
                    LEFT JOIN 
                        Rewards r ON c.CustomerID = r.CustomerID
                    WHERE 
                        m.MembershipLevel = 'Platinum'
                        AND YEAR(t.PurchaseDate) = YEAR(CURRENT_DATE)
                    GROUP BY 
                        c.CustomerID, c.Name;
                """
                cursor.execute(query)
                result = cursor.fetchall()
                
                if result:
                    for row in result:
                        print(f"Customer: {row['Name']}, Reward Check: {row['RewardCheck']}")
                else:
                    print("No platinum customers found.")
        except Error as e:
            print(f"Error while executing the query: {e}")
        finally:
            conn.close()
