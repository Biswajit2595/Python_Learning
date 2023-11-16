import os
import json
import random

# Initialize menu, orders, and user roles as empty lists/dictionary
menu = []
orders = []
user_roles = {'admin': 'admin', 'staff': 'staff', 'cashier': 'cashier'}
current_user_role = None

# Initialize categories for advanced stock management
categories = ['Beverages', 'Snacks', 'Desserts']

# Initialize real-time notifications
notifications = []

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
    category = input(f"Enter category ({', '.join(categories)}): ")

    new_dish = {
        'dish_id': dish_id,
        'dish_name': dish_name,
        'price': price,
        'availability': availability,
        'category': category
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

# Function to display real-time notifications
def display_notifications():
    print("Real-time Notifications:")
    for notification in notifications:
        print(notification)

# Function to authenticate users
def authenticate_user():
    global current_user_role
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username in user_roles and user_roles[username] == password:
        current_user_role = username
        print(f"Welcome, {current_user_role}!")
    else:
        print("Invalid username or password. Access denied.")
        
# Function to logout
def logout():
    global current_user_role
    print(f"Logging out {current_user_role}...")
    exit_program()
    current_user_role = None

# Function to exit the program
def exit_program():
    print("Exiting Mumbai Munchies Plus. Have a great day!")
    exit()

# Main loop
if __name__ == "__main__":
    load_data()
    while True:
        if current_user_role is None:
            authenticate_user()

        if current_user_role == 'admin':
            print("\nMumbai Munchies Plus - Admin Panel")
            print("1. Display Menu")
            print("2. Add Dish to Menu")
            print("3. Remove Dish from Menu")
            print("4. Update Dish Availability")
            print("5. Logout")

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
                logout()
            else:
                print("Invalid choice. Please choose a valid option.")
        
        elif current_user_role == 'staff':
            # Implement staff menu and functionalities
            print("\nMumbai Munchies Plus - Staff")
            print("1. Display Menu")
            print("2. Add Dish to Menu")
            print("3. Update Dish Availability")
            print("4. Logout")

            choice = input("Enter your choice: ")

            if choice == "1":
                display_menu()
            elif choice == "2":
                add_dish()
            elif choice == "3":
                update_availability()
            elif choice == "4":
                logout()
            else:
                print("Invalid choice. Please choose a valid option.")

        elif current_user_role == 'cashier':
            # Implement cashier menu and functionalities
            print("\nMumbai Munchies Plus - Cashier")
            print("1. Display Menu")
            print("2. Logout")
            choice = input("Enter your choice: ")

            if choice == "1":
                display_menu()
            elif choice == "2":
                logout()
            else:
                print("Invalid choice. Please choose a valid option.")
