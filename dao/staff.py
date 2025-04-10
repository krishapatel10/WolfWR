from db.connection import create_connection, close_connection

def enter_staff_info(StaffID, StoreID, Name, JobTitle, Phone, Email, EmploymentDuration, Age, Address):
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO StaffMembers (StaffID, StoreID, Name, JobTitle, Phone, Email, EmploymentDuration, Age, Address)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (StaffID, StoreID, Name, JobTitle, Phone, Email, EmploymentDuration, Age, Address))

        # Insert into subclass table
        job_map = {
            "Manager": "Managers",
            "Assistant Manager": "AssistantManagers",
            "Cashier": "Cashiers",
            "Warehouse Checker": "WarehouseStaff",
            "Billing Staff": "BillingStaff"
        }
        subclass_table = job_map.get(JobTitle)
        if subclass_table:
            cursor.execute(f"INSERT INTO {subclass_table} (StaffID) VALUES (%s)", (StaffID,))

        conn.commit()
        print("Staff inserted successfully.")
    except Exception as e:
        conn.rollback()
        print("Error inserting staff:", e)
    finally:
        cursor.close()
        close_connection(conn)
# Update customer information in the Customers table
def update_customer_info(CustomerID, Name=None, Email=None, Phone=None, Address=None, MembershipLevel=None, ActiveStatus=None):
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor()

        fields = []
        values = []

        if Name is not None:
            fields.append("Name = %s")
            values.append(Name)
        if Email is not None:
            fields.append("Email = %s")
            values.append(Email)
        if Phone is not None:
            fields.append("Phone = %s")
            values.append(Phone)
        if Address is not None:
            fields.append("Address = %s")
            values.append(Address)
        if MembershipLevel is not None:
            fields.append("MembershipLevel = %s")
            values.append(MembershipLevel)
        if ActiveStatus is not None:
            fields.append("ActiveStatus = %s")
            values.append(ActiveStatus)

        if not fields:
            print("Nothing to update.")
            return

        query = f"UPDATE Customers SET {', '.join(fields)} WHERE CustomerID = %s"
        values.append(CustomerID)

        cursor.execute(query, tuple(values))
        conn.commit()
        print("Customer updated successfully.")

    except Exception as e:
        conn.rollback()
        print("Error updating customer:", e)

    finally:
        cursor.close()
        close_connection(conn)


def delete_staff_info(StaffID):
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor()

        # Delete from all subclass tables
        subclass_tables = ["Managers", "AssistantManagers", "Cashiers", "BillingStaff", "WarehouseStaff"]
        for table in subclass_tables:
            cursor.execute(f"DELETE FROM {table} WHERE StaffID = %s", (StaffID,))

        # Delete from Staff
        cursor.execute("DELETE FROM StaffMembers WHERE StaffID = %s", (StaffID,))
        conn.commit()
        print("Staff deleted successfully.")
    except Exception as e:
        conn.rollback()
        print("Error deleting staff:", e)
    finally:
        cursor.close()
        close_connection(conn)
