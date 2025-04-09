import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dao.product import add_product, update_product, delete_product

if __name__ == "__main__":
    add_product(3001, "iPad Pro", 50, 700.00, 899.99, "2026-12-31", 5001)

    # update_product(3001, MarketPrice=849.99)

    # delete_product(3001)
