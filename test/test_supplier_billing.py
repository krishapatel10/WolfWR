import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from transactions.supplier_billing import generate_supplier_bill

if __name__ == "__main__":
    supplier_id = 401  # Try 402 too
    total = generate_supplier_bill(supplier_id)

    if total is not None:
        print(f"✅ Total payable to Supplier {supplier_id}: ${total}")
    else:
        print("❌ Could not generate supplier bill.")
