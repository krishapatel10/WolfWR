import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dao.customer import enter_customer_info, update_customer_info, delete_customer_info

if __name__ == "__main__":
    # Insert a new customer
    # enter_customer_info(1001, "Tejas Desai", "tdesai@ncsu.edu", "9191234567", "Raleigh, NC", "Platinum", True)

    # Update their email and phone
    update_customer_info(1001, Email="newemail@ncsu.edu", Phone="9197654321")

    # Delete the customer
    # delete_customer_info(1001)

