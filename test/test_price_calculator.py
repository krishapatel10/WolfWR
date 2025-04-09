import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.price_calculator import calculate_total_price

if __name__ == "__main__":
    product_ids = [303, 306]  # You can test with products that may/may not be on discount
    total = calculate_total_price(product_ids)

    if total is not None:
        print(f"Total price for products {product_ids}: ${total}")
    else:
        print("Could not calculate total.")

