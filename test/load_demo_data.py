import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dao.customer import enter_customer_info
from dao.staff import enter_staff_info
from dao.store import enter_store_info, update_store_info
from dao.supplier import add_supplier
from dao.product import add_product
from dao.transaction_dao import process_transaction
from dao.signup import add_signup
from dao.discount import add_discount

def load_demo_data():
    # --- Stores ---
    enter_store_info(1001, None, "1021 Main Campus Dr, Raleigh, NC, 27606", "9194789124")
    enter_store_info(1002, None, "851 Partners Way, Raleigh, NC, 27606", "9195929621")

    # --- Staff ---
    staff = [
        (201, 1001, "Alice Johnson", "Manager", "9194285357", "alice.johson@gmail.com", 5, 34, "111 Wolf Street, Raleigh, NC, 27606"),
        (202, 1002, "Bob Smith", "Assistant Manager", "9841482375", "bob.smith@hotmail.com", 3, 29, "222 Fox Ave, Durham, NC, 27701"),
        (203, 1001, "Charlie Davis", "Cashier", "9194856193", "charlie.davis@gmail.com", 7, 40, "333 Bear Rd, Greensboro, NC, 27282"),
        (204, 1002, "David Lee", "Warehouse Checker", "9847028471", "david.lee@yahoo.com", 10, 45, "444 Eagle Dr, Raleigh, NC, 27606"),
        (205, 1001, "Emma White", "Billing Staff", "9198247184", "emma.white@gmail.com", 4, 30, "444 Eagle Dr, Raleigh, NC, 27606"),
        (206, 1002, "Frank Harris", "Billing Staff", "919428535", "frank.harris@gmail.com", 6, 38, "666 Owl Ct, Raleigh, NC, 27610"),
        (207, 1001, "Isla Scott", "Warehouse Checker", "9841298427", "isla.scott@gmail.com", 2, 33, "777 Lynx Rd,Raleigh,NC,27612"),
        (208, 1002, "Jack Lewis", "Cashier", "9194183951", "jack.lewis@gmail.com", 3, 41,"888 Falcon St, Greensboro, NC, 27377"),
    ]
    for s in staff:
        enter_staff_info(*s)
    update_store_info(1001, ManagerID=201)

    # --- Customers ---
    customers = [
        (501, "John Doe", "john.doe@gmail.com", "9194285314", "12 Elm St, Raleigh, NC 27607", "Gold", True),
        (502, "Emily Smith", "emily.smith@gmail.com", "9844235314", "34 Oak Ave, Raleigh, NC 27606", "Silver", False),
        (503, "Michael Brown", "michael.brown@gmail.com", "9194820931", "56 Pine Rd, Raleigh, NC 27607", "Platinum", True),
        (504, "Sarah Johnson", "sarah.johnson@gmail.com", "9841298435", "78 Maple Dr, Raleigh, NC 27607", "Gold", True),
        (505, "David Williams", "david.williams@gmail.com", "9194829424", "90 Birch Ln, Raleigh, NC 27607", "Silver", False),
        (506, "Anna Miller", "anna.miller@gmail.com", "9848519427", "101 Oak Ct, Raleigh, NC 27607", "Platinum", True),
    ]
    for c in customers:
        enter_customer_info(*c)

    # --- Signup ---
    signup = [
        (1001, "2024-01-31", 501),
        (1001, "2022-02-28", 502),
        (1002, "2020-03-22", 503),
        (1002, "2023-03-15", 504),
        (1002, "2024-08-23", 505),
        (1002, "2025-02-10", 506),
    ]
    for s in signup:
        add_signup(*s)

    # --- Suppliers ---
    add_supplier(401, "Fresh Farms Ltd.", "9194248251", "contact@freshfarms.com", "123 Greenway Blvd, Raleigh, NC 27615")
    add_supplier(402, "Organic Good Inc.", "9841384298", "info@orgaincgoods.com", "456 Healthy Rd, Raleigh, NC 27606")

    # --- Products ---
    products = [
        (301, "Organic Apples", 120, 1.5, 2.0, "2025-04-15", 401, "2025-04-12", 1002),
        (302, "Whole Grain Bread", 80, 2.0, 3.5, "2025-04-15", 401, "2025-04-10", 1002),
        (303, "Almond Milk", 150, 3.5, 4.0, "2025-04-30", 401, "2025-04-15", 1002),
        (304, "Brown Rice", 200, 2.8, 3.5, "2026-04-20", 402, "2025-04-12", 1002),
        (305, "Olive Oil", 90, 5.0, 7.0, "2027-04-20", 402, "2025-04-04", 1002),
        (306, "Whole Chicken", 75, 10.0, 13.0, "2025-05-12", 402, "2025-04-12-", 1002),
        (307, "Cheddar Cheese", 60, 3.0, 4.2, "2025-10-12", 402, "2025-04-12-", 1002),
        (308, "Dark Chocolate", 50, 2.5, 3.5, "2026-06-20", 402, "2025-04-12", 1002),
    ]
    for p in products:
        add_product(*p)

    # --- Discounts ---
    discounts = [
        (306, 0.10, "2024-04-10", "2024-05-10"),
        (303, 0.20, "2023-02-12", "2023-02-19"),
    ]
    for d in discounts:
        add_discount(*d)

    # --- Transactions ---
    transactions = [
        (701, 1002, 502, 203, "2024-02-10", 45.00, "Organic Apples, Whole Grain Bread"),
        (702, 1002, 502, 208, "2024-09-12", 60.75, "Almond Milk, Brown Rice, Olive Oil"),
        (703, 1002, 502, 208, "2024-09-23", 78.90, "Almond Milk, Brown Rice, Olive Oil"),
        (704, 1002, 504, 208, "2024-07-23", 32.50, "Whole Chicken"),
    ]
    for t in transactions:
        process_transaction(*t)

    print("✅ All demo data inserted successfully (as per corrected doc).")

if __name__ == "__main__":
    load_demo_data()

