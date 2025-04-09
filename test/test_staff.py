import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dao.staff import enter_staff_info, update_staff_info, delete_staff_info

if __name__ == "__main__":
    enter_staff_info(2001, 1, "Zayaan Siddiqui", "Cashier", "9191112222", "zsiddiq@ncsu.edu", 12)

    # update_staff_info(2001, Email="newzayaan@ncsu.edu", JobTitle="Billing Staff")

    # delete_staff_info(2001)
