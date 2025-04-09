import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from transactions.transfer_stock import transfer_stock

if __name__ == "__main__":
    transfer_stock(301, 1002, 1001, 10)  # e.g., transfer 10 apples from Store 1002 to 1001
