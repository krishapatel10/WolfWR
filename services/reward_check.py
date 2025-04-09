from db.connection import create_connection, close_connection

def generate_platinum_rewards():
    conn = create_connection()
    
    if not conn:
        print("Could not connect to DB.")
        return None
    
    try:
        # Create a cursor to execute the SQL query
        cursor = conn.cursor()
        
        # SQL query to calculate total rewards for Platinum customers in the current year
        query = """
            SELECT
                c.CustomerID,
                c.Name,
                IFNULL(SUM(r.RewardAmount), 0) AS RewardCheck
            FROM
                Customers c
            LEFT JOIN
                Rewards r ON c.CustomerID = r.CustomerID
            WHERE
                c.MembershipLevel = 'Platinum'
                AND c.ActiveStatus = 1
                AND YEAR(r.IssuedDate) = YEAR(CURRENT_DATE)
            GROUP BY
                c.CustomerID, c.Name;
        """
        
        # Execute the query
        cursor.execute(query)
        
        # Fetch all the results
        results = cursor.fetchall()
        
        # Check if there are any results
        if results:
            # Print the result in a formatted way
            for row in results:
                print(f"Customer ID: {row[0]}, Name: {row[1]}, Total Reward: ${row[2]:.2f}")
        else:
            print("No Platinum customers found with rewards for the current year.")
    
    except Exception as e:
        print("Error generating reward checks:", e)
    
    finally:
        # Close the cursor and connection
        cursor.close()
        close_connection(conn)

