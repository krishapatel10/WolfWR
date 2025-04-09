import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reports.sales_report import get_sales_report

if __name__ == "__main__":
    get_sales_report('month')  # Try 'day' or 'year'
