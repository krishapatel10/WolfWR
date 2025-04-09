from db.connection import create_connection, close_connection

def test_db():
    conn = create_connection()
    if conn:
        print("Successfully connected to MariaDB!")
        close_connection(conn)
    else:
        print("Connection failed.")

if __name__ == "__main__":
    test_db()
