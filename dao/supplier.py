from db.connection import create_connection, close_connection

def add_supplier(SupplierID, Name, Phone, Email, Location):
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO Suppliers (SupplierID, Name, Phone, Email, Location)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (SupplierID, Name, Phone, Email, Location))
        conn.commit()
        print("Supplier added successfully.")
    except Exception as e:
        conn.rollback()
        print("Error adding supplier:", e)
    finally:
        cursor.close()
        close_connection(conn)


def delete_supplier(SupplierID):
    conn = create_connection()
    if not conn:
        print("Could not connect to DB.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Suppliers WHERE SupplierID = %s", (SupplierID,))
        conn.commit()
        print("Supplier deleted successfully.")
    except Exception as e:
        conn.rollback()
        print("Error deleting supplier:", e)
    finally:
        cursor.close()
        close_connection(conn)

def update_supplier(SupplierID, Name=None, Phone=None, Email=None, Location=None):
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
        if Phone is not None:
            fields.append("Phone = %s")
            values.append(Phone)
        if Email is not None:
            fields.append("Email = %s")
            values.append(Email)
        if Location is not None:
            fields.append("Location = %s")
            values.append(Location)

        if not fields:
            print("Nothing to update.")
            return

        query = f"UPDATE Suppliers SET {', '.join(fields)} WHERE SupplierID = %s"
        values.append(SupplierID)
        cursor.execute(query, tuple(values))

        conn.commit()
        print("Supplier updated successfully.")
    except Exception as e:
        conn.rollback()
        print("Error updating supplier:", e)
    finally:
        cursor.close()
        close_connection(conn)
