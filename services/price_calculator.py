from db.connection import create_connection, close_connection
from datetime import datetime
from decimal import Decimal

def calculate_total_price_with_discount(transaction_id):
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        conn.start_transaction() 

        # Get transaction items
        cursor.execute("""
            SELECT ti.ProductID, ti.Quantity, ti.UnitPrice
            FROM TransactionItems ti
            WHERE ti.TransactionID = %s
        """, (transaction_id,))
        items = cursor.fetchall()

        if not items:
            conn.rollback()
            print(f"No items found for transaction {transaction_id}")
            return 0.0

        # Get the purchase date
        cursor.execute("""
            SELECT PurchaseDate FROM Transactions WHERE TransactionID = %s
        """, (transaction_id,))
        transaction = cursor.fetchone()

        if not transaction:
            conn.rollback()
            print(f"Transaction {transaction_id} not found")
            return 0.0

        total_price = 0.0
        purchase_date = transaction['PurchaseDate']

        for item in items:
            cursor.execute("""
                SELECT DiscountRate 
                FROM Discounts 
                WHERE ProductID = %s 
                AND %s BETWEEN ValidFrom AND ValidTo
            """, (item['ProductID'], purchase_date))
            discount = cursor.fetchone()
            rate = discount['DiscountRate'] if discount else 0.0
            discounted_price = item['UnitPrice'] * (1 - rate / 100)
            total_price += discounted_price * item['Quantity']

        conn.commit()  # Commit even for read integrity
        return round(total_price, 2)

    except Exception as e:
        print("Error calculating total price with discount:", e)
        conn.rollback()  # Rollback on failure
        return None
    finally:
        cursor.close()
        close_connection(conn)
