import pymysql
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_connection():
    try:
        connection = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT")),
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Connection successful!")
        return connection
    except Exception as e:
        print("Connection failed:", e)
        return None

# Example usage
if __name__ == "__main__":
    conn = get_connection()
    if conn:
        conn.close()
