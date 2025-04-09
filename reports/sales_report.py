from db.connection import create_connection, close_connection

from db.connection import create_connection, close_connection
from decimal import Decimal

def generate_sales_report_by_day():
    """
    Generates a sales report grouped by day.
    Each day's total sales are calculated and returned.
    """
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor(dictionary=True)

        # SQL query to get total sales by day
        cursor.execute("""
            SELECT DATE(PurchaseDate) AS SaleDate, SUM(TotalPrice) AS TotalSales
            FROM Transactions
            GROUP BY DATE(PurchaseDate)
            ORDER BY SaleDate;
        """)

        # Fetch all results
        results = cursor.fetchall()
        
        if results:
            print("\n=== SALES REPORT BY DAY ===")
            for row in results:
                sale_date = row['SaleDate']
                total_sales = Decimal(row['TotalSales']).quantize(Decimal('0.00'))
                print(f"Date: {sale_date} | Total Sales: ${total_sales}")
        else:
            print("No sales data found.")

    except Exception as e:
        print(f"\nReport generation failed: {str(e)}")
    finally:
        cursor.close()
        close_connection(conn)


def generate_sales_report_by_month():
    """
    Generates a sales report grouped by month and year.
    Each month's total sales are calculated and returned.
    """
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor(dictionary=True)

        # SQL query to get total sales by month
        cursor.execute("""
            SELECT YEAR(PurchaseDate) AS Year, MONTH(PurchaseDate) AS Month, SUM(TotalPrice) AS TotalSales
            FROM Transactions
            GROUP BY YEAR(PurchaseDate), MONTH(PurchaseDate)
            ORDER BY Year, Month;
        """)

        # Fetch all results
        results = cursor.fetchall()

        if results:
            print("\n=== SALES REPORT BY MONTH ===")
            for row in results:
                year = row['Year']
                month = row['Month']
                total_sales = Decimal(row['TotalSales']).quantize(Decimal('0.00'))
                print(f"Year: {year} | Month: {month} | Total Sales: ${total_sales}")
        else:
            print("No sales data found.")

    except Exception as e:
        print(f"\nReport generation failed: {str(e)}")
    finally:
        cursor.close()
        close_connection(conn)

def generate_sales_report_by_year():
    """
    Generates a sales report grouped by year.
    Each year's total sales are calculated and returned.
    """
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor(dictionary=True)

        # SQL query to get total sales by year
        cursor.execute("""
            SELECT YEAR(PurchaseDate) AS Year, SUM(TotalPrice) AS TotalSales
            FROM Transactions
            GROUP BY YEAR(PurchaseDate)
            ORDER BY Year;
        """)

        # Fetch all results
        results = cursor.fetchall()

        if results:
            print("\n=== SALES REPORT BY YEAR ===")
            for row in results:
                year = row['Year']
                total_sales = Decimal(row['TotalSales']).quantize(Decimal('0.00'))
                print(f"Year: {year} | Total Sales: ${total_sales}")
        else:
            print("No sales data found.")

    except Exception as e:
        print(f"\nReport generation failed: {str(e)}")
    finally:
        cursor.close()
        close_connection(conn)
