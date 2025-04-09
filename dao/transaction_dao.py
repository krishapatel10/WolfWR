from decimal import Decimal
from db.connection import create_connection, close_connection
from datetime import datetime

def add_transaction(store_id, customer_id, cashier_id, purchase_date, items):
    """
    Processes a complete transaction using the correct Inventory table structure
    """
    conn = None
    cursor = None
    
    try:
        # 1. Establish connection
        conn = create_connection()
        if not conn:
            print("Could not connect to DB.")
            return None

        cursor = conn.cursor(dictionary=True)
        conn.start_transaction()

        # 2. Validate customer
        cursor.execute("""
            SELECT MembershipLevel, ActiveStatus, Name 
            FROM Customers 
            WHERE CustomerID = %s
        """, (customer_id,))
        customer = cursor.fetchone()

        if not customer:
            raise Exception(f"Customer {customer_id} not found")
        if not customer['ActiveStatus']:
            raise Exception(f"Customer {customer['Name']} is inactive")

        # 3. Determine membership reward rate
        reward_rate = Decimal({
            'Platinum': '5',
            'Gold': '3',
            'Silver': '1'
        }.get(customer['MembershipLevel'], '0'))

        # 4. Calculate transaction amounts
        subtotal = Decimal('0.00')
        product_discounts = Decimal('0.00')
        receipt_items = []

        for item in items:
            product_id = int(item['product_id'])
            quantity = int(item['quantity'])

            # Get product info
            cursor.execute("""
                SELECT Name, MarketPrice, 
                       (SELECT DiscountRate FROM Discounts 
                        WHERE ProductID = %s 
                        AND %s BETWEEN ValidFrom AND ValidTo) AS DiscountRate
                FROM Products 
                WHERE ProductID = %s
            """, (product_id, purchase_date, product_id))
            product = cursor.fetchone()

            if not product:
                raise Exception(f"Product {product_id} not found")

            # Calculate pricing
            unit_price = Decimal(str(product['MarketPrice']))
            discount_rate = Decimal(str(product['DiscountRate'] or '0'))
            discount_amount = unit_price * (discount_rate / Decimal('100'))
            final_price = unit_price - discount_amount
            item_total = quantity * final_price

            subtotal += item_total
            product_discounts += quantity * discount_amount

            receipt_items.append({
                'name': product['Name'],
                'quantity': quantity,
                'unit_price': unit_price,
                'discount_rate': discount_rate,
                'total': item_total
            })

        # Calculate reward (doesn't affect total)
        reward_amount = (subtotal * reward_rate / Decimal('100')).quantize(Decimal('0.00'))
        total_price = subtotal

        # 5. Insert transaction
        cursor.execute("""
            INSERT INTO Transactions (StoreID, CustomerID, CashierID, PurchaseDate, TotalPrice)
            VALUES (%s, %s, %s, %s, %s)
        """, (store_id, customer_id, cashier_id, purchase_date, float(total_price)))

        transaction_id = cursor.lastrowid

        # 6. Process items and inventory (using StockQuantity)
        for item in items:
            product_id = int(item['product_id'])
            quantity = int(item['quantity'])

            cursor.execute("SELECT MarketPrice FROM Products WHERE ProductID = %s", (product_id,))
            unit_price = Decimal(str(cursor.fetchone()['MarketPrice']))

            # Insert transaction item
            cursor.execute("""
                INSERT INTO TransactionItems 
                (TransactionID, ProductID, Quantity, UnitPrice)
                VALUES (%s, %s, %s, %s)
            """, (transaction_id, product_id, quantity, float(unit_price)))

            # Update inventory using StockQuantity
            cursor.execute("""
                UPDATE Inventory 
                SET StockQuantity = StockQuantity - %s
                WHERE StoreID = %s AND ProductID = %s
            """, (quantity, store_id, product_id))

            # Verify inventory using StockQuantity
            cursor.execute("""
                SELECT StockQuantity FROM Inventory 
                WHERE StoreID = %s AND ProductID = %s
            """, (store_id, product_id))
            if cursor.fetchone()['StockQuantity'] < 0:
                raise Exception(f"Insufficient stock for product {product_id}")

        # 7. Record reward if applicable
        if reward_rate > 0:
            cursor.execute("""
                INSERT INTO Rewards 
                (CustomerID, RewardAmount, IssuedDate)
                VALUES (%s, %s, %s)
            """, (customer_id, float(reward_amount), purchase_date))

        conn.commit()

        # 8. Generate receipt
        print("\n=== TRANSACTION RECEIPT ===")
        print(f"Transaction #: {transaction_id}")
        print(f"Date: {purchase_date}")
        print(f"Customer: {customer['Name']} ({customer['MembershipLevel']})")
        print("\nITEMS PURCHASED:")
        for item in receipt_items:
            print(f"{item['quantity']} x {item['name']}")
            print(f"  ${item['unit_price']:.2f} each", end='')
            if item['discount_rate'] > 0:
                print(f" (Discount: {item['discount_rate']}%)", end='')
            print(f" → ${item['total']:.2f}")

        print("\nSUMMARY:")
        print(f"Subtotal: ${subtotal:.2f}")
        if product_discounts > 0:
            print(f"Product Discounts: -${product_discounts:.2f}")
        print(f"Total: ${total_price:.2f}")
        if reward_rate > 0:
            print(f"Membership Reward Earned: ${reward_amount:.2f} ({reward_rate}% of purchase)")

        return transaction_id

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"\nTransaction failed: {str(e)}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            close_connection(conn)