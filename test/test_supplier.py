import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dao.supplier import add_supplier

if __name__ == "__main__":
    add_supplier(
        SupplierID=5001,
        Name="Apple Inc.",
        Phone="800MYAPPLE",
        Email="supply@apple.com",
        Location="Cupertino, CA"
    )
