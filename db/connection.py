import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='classdb2.csc.ncsu.edu',
            port=3306,
            database='kpatel46',
            user='kpatel46',
            password='540projectTeam'
        )
        return connection
    except Error as e:
        print(f"Connection error: {e}")
        return None

def close_connection(conn):
    if conn and conn.is_connected():
        conn.close()
