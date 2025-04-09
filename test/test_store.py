import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dao.store import enter_store_info, update_store_info, delete_store_info

if __name__ == "__main__":
    # enter_store_info(1, 2001, "Raleigh, NC", "9190000000")

    update_store_info(1, ManagerID=2001)

    # delete_store_info(1)
