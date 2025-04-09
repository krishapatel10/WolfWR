import sys
import os
from decimal import Decimal
from datetime import datetime

# Adjust sys.path to ensure the db module is found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.connection import create_connection, close_connection
from dao.transaction_dao import add_transaction

def test_transaction():
    # Test data using existing IDs from your schema
    transaction_data = {
        'store_id': 1002,
        'customer_id': 501,  # John Doe (Active Gold)
        'cashier_id': 203,
        'purchase_date': '2024-04-15',
        'items': [
            {'product_id': 301, 'quantity': 2},  # Organic Apples
            {'product_id': 302, 'quantity': 1}   # Whole Grain Bread
        ]
    }
    
    result = add_transaction(**transaction_data)
    if result:
        print(f"Transaction successful! ID: {result}")
    else:
        print("Transaction failed")

if __name__ == "__main__":
    test_transaction()