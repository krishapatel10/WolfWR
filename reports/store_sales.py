from db.connection import create_connection, close_connection

from db.connection import create_connection, close_connection
from decimal import Decimal

def generate_sales_report_for_store(store_id, start_date, end_date):
    """
    Generates a sales report for a specific store within a given time period.
    The report calculates total sales for each day within the date range.
    """
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor(dictionary=True)

        # SQL query to get total sales for a specific store and date range
        cursor.execute("""
            SELECT DATE(PurchaseDate) AS SaleDate, SUM(TotalPrice) AS TotalSales
            FROM Transactions
            WHERE StoreID = %s AND PurchaseDate BETWEEN %s AND %s
            GROUP BY DATE(PurchaseDate)
            ORDER BY SaleDate;
        """, (store_id, start_date, end_date))

        # Fetch all results
        results = cursor.fetchall()

        if results:
            print(f"\n=== SALES REPORT FOR STORE {store_id} ===")
            print(f"From {start_date} to {end_date}\n")
            for row in results:
                sale_date = row['SaleDate']
                total_sales = Decimal(row['TotalSales']).quantize(Decimal('0.00'))
                print(f"Date: {sale_date} | Total Sales: ${total_sales}")
        else:
            print("No sales data found for the specified period.")

    except Exception as e:
        print(f"\nReport generation failed: {str(e)}")
    finally:
        cursor.close()
        close_connection(conn)
