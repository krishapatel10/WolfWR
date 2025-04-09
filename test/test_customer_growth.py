import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reports.customer_growth import get_customer_growth_report

if __name__ == "__main__":
    get_customer_growth_report("month")
    get_customer_growth_report("year")
