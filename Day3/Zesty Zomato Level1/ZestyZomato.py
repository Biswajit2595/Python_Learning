import os
import json
import random

# Initialize menu and orders as empty lists
menu = []
orders = []

def load_data():
    global menu, orders
    if os.path.exists("menu.json"):
        with open("menu.json", "r") as menu_file:
            menu = json.load(menu_file)

    if os.path.exists("orders.json"):
        try:
            with open("orders.json", "r") as orders_file:
                orders = json.load(orders_file)
        except json.decoder.JSONDecodeError:
            orders = []


# Function to save data to a file
def save_data():
    with open("menu.json", "w") as menu_file:
        json.dump(menu, menu_file, indent=4)
    with open("orders.json", "w") as orders_file:
        json.dump(orders, orders_file, indent=4)

# Function to display the menu
def display_menu():
    print("Menu:")
    for item in menu:
        print(f"{item['dish_id']}: {item['dish_name']} - ₹{item['price']} ({'Available' if item['availability'] else 'Not Available'})")

# Function to add a new dish to the menu
def add_dish():
    dish_id = input("Enter Dish ID: ")
    dish_name = input("Enter Dish Name: ")
    price = float(input("Enter Price: ₹"))
    availability = input("Is it available? (yes/no): ").lower() == "yes"

    new_dish = {
        'dish_id': dish_id,
        'dish_name': dish_name,
        'price': price,
        'availability': availability
    }

    menu.append(new_dish)
    save_data()
    print(f"{dish_name} has been added to the menu.")

# Function to remove a dish from the menu
def remove_dish():
    display_menu()
    dish_id = input("Enter Dish ID to remove: ")
    for item in menu:
        if item['dish_id'] == dish_id:
            menu.remove(item)
            save_data()
            print(f"Dish with ID {dish_id} has been removed from the menu.")
            return
    print(f"No dish found with ID {dish_id}.")

# Function to update the availability of a dish
def update_availability():
    display_menu()
    dish_id = input("Enter Dish ID to update availability: ")
    for item in menu:
        if item['dish_id'] == dish_id:
            availability = input("Update availability (yes/no): ").lower() == "yes"
            item['availability'] = availability
            save_data()
            print(f"Availability of {item['dish_name']} updated.")
            return
    print(f"No dish found with ID {dish_id}.")
    
    
def place_order():
    display_menu()
    customer_name = input("Enter Customer Name: ")
    input_dish_ids = input("Enter Dish IDs (comma-separated): ").split(',')
    order_id = len(orders) + 1  # Set the order_id once before the loop
    order_status = "received"
    dish_ids = []

    for input_dish_id in input_dish_ids:
        dish_id = int(input_dish_id)
        # Check if the dish_id is valid by looking it up in the menu
        dish_exists = any(item['dish_id'] == dish_id for item in menu)
        
        if dish_exists:
            dish_ids.append(dish_id)
        else:
            print(f"Invalid dish ID {dish_id}. Skipping.")
    
    if not dish_ids:
        print("No valid dish IDs provided. Order not placed.")
        return

    order = {
        'order_id': order_id,  # Use the same order_id for all dishes in this order
        'customer_name': customer_name,
        'dish_ids': dish_ids,
        'order_status': order_status,
    }
    
    orders.append(order)
    save_data()
    
    for dish_id in dish_ids:
        for item in menu:
            if item['dish_id'] == dish_id:
                if item['availability']:
                    print(f"Order {order_id} placed for {item['dish_name']}.")
                else:
                    print(f"{item['dish_name']} is not available.")
                break
        else:
            print(f"No dish found with ID {dish_id}.")



# Function to update the status of an order
def update_order_status():
    order_id = input("Enter Order ID to update status: ")
    new_status = input("Update status (received/preparing/ready for pickup/delivered): ").lower()
    updated = False

    for order in orders:
        if order['order_id'] == int(order_id):
            order['order_status'] = new_status
            updated = True

    if updated:
        save_data()
        print(f"Status of Order ID {order_id} have been updated to {new_status}.")
    else:
        print(f"No orders found with Order ID {order_id}.")

# Main loop
if __name__ == "__main__":
    load_data()
    while True:
        print("\nZesty Zomato: The Great Food Fiasco")
        print("1. Display Menu")
        print("2. Add Dish to Menu")
        print("3. Remove Dish from Menu")
        print("4. Update Dish Availability")
        print("5. Place Order")
        print("6. Update Order Status")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            display_menu()
        elif choice == "2":
            add_dish()
        elif choice == "3":
            remove_dish()
        elif choice == "4":
            update_availability()
        elif choice == "5":
            place_order()
        elif choice == "6":
            update_order_status()
        elif choice == "7":
            print("Exiting Zesty Zomato. Have a great day!")
            break
        else:
            print("Invalid choice. Please choose a valid option.")

