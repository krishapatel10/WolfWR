import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reports.store_sales import get_store_sales_growth

if __name__ == "__main__":
    get_store_sales_growth(1002, "month")
    get_store_sales_growth(1002, "year")
