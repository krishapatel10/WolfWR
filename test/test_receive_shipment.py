import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from transactions.receive_shipment import receive_shipment

if __name__ == "__main__":
    receive_shipment(
        shipment_id=6001,
        product_id=3001,
        supplier_id=5001,
        store_id=1,
        quantity_received=10
    )
