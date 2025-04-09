from db.connection import create_connection, close_connection

def add_discount(DiscountID, ProductID, DiscountRate, ValidFrom, ValidTo):
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO Discounts (DiscountID, ProductID, DiscountRate, ValidFrom, ValidTo)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (DiscountID, ProductID, DiscountRate, ValidFrom, ValidTo))
        conn.commit()
        print("Discount added successfully.")
    except Exception as e:
        conn.rollback()
        print("Error adding discount:", e)
    finally:
        cursor.close()
        close_connection(conn)

def get_expired_discounts():
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM Discounts WHERE ValidTo < CURDATE()"
        cursor.execute(query)
        results = cursor.fetchall()
        if results:
            print("Expired Discounts:")
            for row in results:
                print(row)
        else:
            print("No expired discounts.")
        return results
    except Exception as e:
        print("Error fetching expired discounts:", e)
        return []
    finally:
        cursor.close()
        close_connection(conn)


def delete_expired_discounts():
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor()
        query = "DELETE FROM Discounts WHERE ValidTo < CURDATE()"
        cursor.execute(query)
        conn.commit()
        print(f"{cursor.rowcount} expired discount(s) deleted.")
    except Exception as e:
        conn.rollback()
        print("Error deleting expired discounts:", e)
    finally:
        cursor.close()
        close_connection(conn)
