import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reports.transfer_report import get_transfer_report

if __name__ == "__main__":
    get_transfer_report()
