from db.connection import create_connection, close_connection
from datetime import datetime

from db.connection import create_connection, close_connection

def customer_activity_report(start_date, end_date):
    """
    Generates a report of customer activity between the given start and end dates.
    Includes total purchase amount and number of transactions per customer.
    """
    conn = create_connection()
    if not conn:
        print("Failed to connect to database.")
        return

    try:
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                CustomerID,
                COUNT(*) AS TransactionsCount,
                SUM(TotalPrice) AS TotalSpent
            FROM Transactions
            WHERE PurchaseDate BETWEEN %s AND %s
            GROUP BY CustomerID
            ORDER BY TotalSpent DESC;
        """
        cursor.execute(query, (start_date, end_date))
        results = cursor.fetchall()

        if results:
            print(f"Customer Activity Report from {start_date} to {end_date}:\n")
            for row in results:
                print(f"Customer {row['CustomerID']} - Transactions: {row['TransactionsCount']}, Total Spent: ${row['TotalSpent']:.2f}")
        else:
            print(f"No transactions found between {start_date} and {end_date}.")

    except Exception as e:
        print(f"Error occurred: {str(e)}")
    finally:
        cursor.close()
        close_connection(conn)



def get_total_spent_currentday():
    """
    Calculates the total amount spent today based on transaction records.
    """
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor()

        # Get today's date
        today_date = datetime.now().strftime('%Y-%m-%d')

        # SQL query to sum the amount for today's transactions
        cursor.execute("""
            SELECT SUM(TotalPrice) AS TotalAmountSpent
            FROM Transactions
            WHERE DATE(PurchaseDate) = %s;
        """, (today_date,))

        result = cursor.fetchone()

        if result and result['TotalAmountSpent']:
            print(f"Total amount spent today from transactions: ${result['TotalAmountSpent']:.2f}")
        else:
            print("No transactions found for today.")

    except Exception as e:
        print(f"Error occurred: {str(e)}")
    finally:
        cursor.close()
        close_connection(conn)


def get_total_spent_current_year_():
    """
    Calculates the total amount spent by each customer within the current year.
    """
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor(dictionary=True)

        # Get the current year
        current_year = datetime.now().year

        # SQL query to sum the amount spent by each customer in the current year
        cursor.execute("""
            SELECT CustomerID, SUM(TotalPrice) AS TotalAmountSpent
            FROM Transactions
            WHERE YEAR(PurchaseDate) = %s
            GROUP BY CustomerID;
        """, (current_year,))

        results = cursor.fetchall()

        if results:
            print(f"Total Amount Spent by Each Customer in {current_year}:")
            for row in results:
                customer_id = row['CustomerID']
                total_spent = row['TotalAmountSpent']
                print(f"Customer {customer_id} has spent ${total_spent:.2f} this year.")
        else:
            print(f"No transactions found for any customer this year.")

    except Exception as e:
        print(f"Error occurred: {str(e)}")
    finally:
        cursor.close()
        close_connection(conn)

