from db.connection import create_connection, close_connection

def generate_customer_growth_report_by_month():
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor(dictionary=True)
        # SQL query to get customer growth by month
        cursor.execute("""
            SELECT 
                YEAR(ActivationDate) AS Year,
                MONTH(ActivationDate) AS Month,
                COUNT(CustomerID) AS NewCustomers
            FROM 
                Memberships
            WHERE 
                ActiveStatus = 1 
            GROUP BY 
                YEAR(ActivationDate), MONTH(ActivationDate)
            ORDER BY 
                Year, Month;""")
        results = cursor.fetchall()

        if results:
            print("CUSTOMER GROWTH REPORT BY MONTH")
            for row in results:
                year = row['Year']
                month = row['Month']
                new_customers = row['NewCustomers']
                print(f"Year: {year}| Month: {month} | New Customers: {new_customers}")
        else:
            print("No customer growth data found.")

    except Exception as e:
        print(f"\nReport generation failed: {str(e)}")
    finally:
        cursor.close()
        close_connection(conn)



def generate_customer_growth_report_by_year():
    """
    Generates a customer growth report by year.
    The report includes the year and the number of new customers for each year.
    """
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor(dictionary=True)

        # SQL query to get customer growth by year
        cursor.execute("""SELECT 
                YEAR(ActivationDate) AS Year,
                COUNT(CustomerID) AS NewCustomers
            FROM 
                Memberships
            WHERE 
                ActiveStatus = 1 
            GROUP BY 
                YEAR(ActivationDate)
            ORDER BY 
                Year;""")

        # Fetch all results
        results = cursor.fetchall()

        if results:
            print("=== CUSTOMER GROWTH REPORT BY YEAR ===")
            for row in results:
                year = row['Year']
                new_customers = row['NewCustomers']

                # Print the customer growth details by year
                print(f"Year: {year} | New Customers: {new_customers}")
        else:
            print("No customer growth data found.")

    except Exception as e:
        print(f"\nReport generation failed: {str(e)}")
    finally:
        cursor.close()
        close_connection(conn)
