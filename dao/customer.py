from db.connection import create_connection, close_connection

# Insert a new customer into the Customers table
def enter_customer_info(CustomerID, Name, Email, Phone, Address, MembershipLevel, ActiveStatus):
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor()

        query = """
        INSERT INTO Customers (CustomerID, Name, Email, Phone, Address, MembershipLevel, ActiveStatus)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (CustomerID, Name, Email, Phone, Address, MembershipLevel, ActiveStatus))
        conn.commit()
        print("Customer inserted successfully.")

    except Exception as e:
        conn.rollback()
        print("Error inserting customer:", e)

    finally:
        cursor.close()
        close_connection(conn)


def add_membership_info(MembershipID, CustomerID, SignupStoreID, ActivationDate, ExpirationDate, MembershipLevel, ActiveStatus):
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor()

        # Insert into Memberships table
        query = """
        INSERT INTO Memberships (MembershipID, CustomerID, SignupStoreID, ActivationDate, ExpirationDate, MembershipLevel, ActiveStatus)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (MembershipID, CustomerID, SignupStoreID, ActivationDate, ExpirationDate, MembershipLevel, ActiveStatus))

        # Update customer ActiveStatus to 1
        update_query = "UPDATE Customers SET ActiveStatus = 1 WHERE CustomerID = %s"
        cursor.execute(update_query, (CustomerID,))

        conn.commit()
        print("Membership added and customer activated.")

    except Exception as e:
        conn.rollback()
        print("Error inserting membership or updating customer:", e)

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

# Delete customer information from the Customers table
def delete_customer_info(CustomerID):
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor()
        query = "DELETE FROM Customers WHERE CustomerID = %s"
        cursor.execute(query, (CustomerID,))
        conn.commit()
        print("Customer deleted successfully.")
    except Exception as e:
        conn.rollback()
        print("Error deleting customer:", e)
    finally:
        cursor.close()
        close_connection(conn)


# Update membership status when the membership is expired
def update_membership_status():
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor()

        # Update membership to inactive if the expiration date is before today
        query_update = """
        UPDATE Memberships
        SET ActiveStatus = 0
        WHERE ExpirationDate < CURDATE() AND ActiveStatus = 1
        """
        cursor.execute(query_update)
        conn.commit()
        print("Expired memberships have been deactivated.")

    except Exception as e:
        conn.rollback()
        print("Error updating membership status:", e)

    finally:
        cursor.close()
        close_connection(conn)

