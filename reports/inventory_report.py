from db.connection import create_connection, close_connection

from db.connection import create_connection, close_connection

def generate_product_stock_report(product_id):
    """
    Generates a merchandise stock report for a specific product.
    The report includes the product name, store ID, stock quantity, and last stock update.
    """
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor(dictionary=True)

        # SQL query to get stock information for the specified product
        cursor.execute("""
            SELECT 
                p.ProductID,
                p.Name AS ProductName,
                i.StoreID,
                i.StockQuantity,
                i.LastStockUpdate
            FROM 
                Products p
            JOIN 
                Inventory i ON p.ProductID = i.ProductID
            WHERE 
                p.ProductID = %s;
        """, (product_id,))

        # Fetch all results
        results = cursor.fetchall()

        if results:
            print(f"\n=== MERCHANDISE STOCK REPORT FOR PRODUCT ID {product_id} ===")
            for row in results:
                product_name = row['ProductName']
                store_id = row['StoreID']
                stock_quantity = row['StockQuantity']
                last_update = row['LastStockUpdate']

                # Print the product stock details for the specified product
                print(f"Product Name: {product_name} | Store ID: {store_id} | Available Stock: {stock_quantity} | Last Stock Update: {last_update}")
        else:
            print(f"No stock data found for Product ID {product_id}.")

    except Exception as e:
        print(f"\nReport generation failed: {str(e)}")
    finally:
        cursor.close()
        close_connection(conn)



from db.connection import create_connection, close_connection

def generate_store_stock_report():
    """
    Generates a merchandise stock report for each store.
    The report includes the store ID, product name, stock quantity, and last stock update.
    """
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor(dictionary=True)

        # SQL query to get stock information for all stores and products
        cursor.execute("""
            SELECT 
                i.StoreID,
                p.ProductID,
                p.Name AS ProductName,
                i.StockQuantity,
                i.LastStockUpdate
            FROM 
                Inventory i
            JOIN 
                Products p ON i.ProductID = p.ProductID
            ORDER BY 
                i.StoreID, p.ProductID;
        """)

        # Fetch all results
        results = cursor.fetchall()

        if results:
            print("=== MERCHANDISE STOCK REPORT FOR EACH STORE ===")
            for row in results:
                store_id = row['StoreID']
                product_name = row['ProductName']
                stock_quantity = row['StockQuantity']
                last_update = row['LastStockUpdate']

                # Print the stock details for each product in each store
                print(f"Store ID: {store_id} | Product Name: {product_name} | Available Stock: {stock_quantity} | Last Stock Update: {last_update}")
        else:
            print("No stock data found.")

    except Exception as e:
        print(f"\nReport generation failed: {str(e)}")
    finally:
        cursor.close()
        close_connection(conn)
