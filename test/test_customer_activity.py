import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reports.customer_activity import get_customer_activity_report

if __name__ == "__main__":
    get_customer_activity_report("2024-01-01", "2024-12-31")
