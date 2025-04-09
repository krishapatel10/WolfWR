import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from transactions.refund_processor import process_refund

if __name__ == "__main__":
    process_refund(703, 303, 2)  # Refund 2x Almond Milk from transaction 703
