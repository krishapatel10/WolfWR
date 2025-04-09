import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reports.inventory_report import get_inventory_report

if __name__ == "__main__":
    get_inventory_report()           # All stores
    get_inventory_report(1002)       # Specific store
