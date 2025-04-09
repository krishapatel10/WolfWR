import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from transactions.purchase_flow import purchase_product

if __name__ == "__main__":
    purchase_product(
        customer_id=1001,
        product_id=3001,
        store_id=1,
        cashier_id=2001,
        quantity=1,
        transaction_id=5001
    )
