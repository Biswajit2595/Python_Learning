import hashlib
import os
import json
import getpass
import matplotlib.pyplot as plt

# Define lists and dictionaries for snack inventory and sales records
snack_inventory = []
sales_records = []
notifications = []

# Define a dictionary to store user roles and their privileges
user_roles = {
    "admin": {
        "add_snack": True,
        "remove_snack": True,
        "update_availability": True,
        "record_sale": True,
        "generate_report": True,
    },
    "canteen_staff": {
        "add_snack": True,
        "remove_snack": False,
        "update_availability": True,
        "record_sale": True,
        "generate_report": False,
    },
    "cashier": {
        "add_snack": False,
        "remove_snack": False,
        "update_availability": False,
        "record_sale": True,
        "generate_report": False,
    },
}

# Define a dictionary to store user data (replace with hashed passwords)
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "staff1": {"password": "staff123", "role": "canteen_staff"},
    "cashier1": {"password": "cashier123", "role": "cashier"},
}

# Define a function to authenticate users
def authenticate_user():
    while True:
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")

        if username in users and hashlib.md5(password.encode()).hexdigest() == hashlib.md5(users[username]["password"].encode()).hexdigest():
            return users[username]["role"]
        else:
            print("Authentication failed. Please enter valid credentials.")

# Define a function to display the menu based on the user's role
def show_menu(user_role):
    print("\nCanteen Snack Inventory Management")
    print("1. Add Snack" if user_roles[user_role]["add_snack"] else "")
    print("2. Remove Snack" if user_roles[user_role]["remove_snack"] else "")
    print("3. Update Snack Availability")
    print("4. Record Sales")
    print("5. Generate Sales Report" if user_roles[user_role]["generate_report"] else "")
    print("6. Exit")

# Define a function to add snacks to the inventory
def add_snack():
    snack_id = input("Enter Snack ID: ")
    snack_name = input("Enter Snack Name: ")
    price = float(input("Enter Snack Price: "))
    available = input("Is the snack available? (yes/no): ").lower()

    snack = {
        "id": snack_id,
        "name": snack_name,
        "price": price,
        "available": available == "yes",
    }

    snack_inventory.append(snack)
    print(f"{snack_name} has been added to the inventory.")
    notifications.append(f"Added snack: {snack_name}")

# Define a function to remove snacks from the inventory
def remove_snack():
    snack_id = input("Enter Snack ID to remove: ")
    for snack in snack_inventory:
        if snack["id"] == snack_id:
            snack_inventory.remove(snack)
            print(f"Snack with ID {snack_id} has been removed from the inventory.")
            notifications.append(f"Removed snack with ID {snack_id}")
            return
    print(f"Snack with ID {snack_id} not found in the inventory.")
    notifications.append(f"Failed to remove snack with ID {snack_id}")

# Define a function to update snack availability
def update_availability():
    snack_id = input("Enter Snack ID to update availability: ")
    for snack in snack_inventory:
        if snack["id"] == snack_id:
            available = input("Is the snack available? (yes/no): ").lower()
            snack["available"] = available == "yes"
            print(f"Availability of snack with ID {snack_id} has been updated.")
            notifications.append(f"Updated availability of snack with ID {snack_id}")
            return
    print(f"Snack with ID {snack_id} not found in the inventory.")
    notifications.append(f"Failed to update availability for snack with ID {snack_id}")

# Define a function to record snack sales
def record_sale():
    snack_id = input("Enter Snack ID sold: ")
    quantity = int(input("Enter the quantity sold: "))

    for snack in snack_inventory:
        if snack["id"] == snack_id:
            if snack["available"]:
                sales_records.append((snack_id, quantity))
                print(f"Sales of {quantity} {snack['name']} recorded.")
                notifications.append(f"Recorded sales of {quantity} {snack['name']}")
                return
            else:
                print(f"{snack['name']} is not available for sale.")
                notifications.append(f"Failed to record sales for {snack['name']} as it is unavailable.")
                return
    print(f"Snack with ID {snack_id} not found in the inventory.")
    notifications.append(f"Failed to record sales for snack with ID {snack_id}")

# Define a function to generate and display a sales report
def generate_report():
    report_data = {}
    for sale in sales_records:
        snack = next((s for s in snack_inventory if s['id'] == sale[0]), None)
        if snack:
            snack_name = snack['name']
            if snack_name not in report_data:
                report_data[snack_name] = 0
            report_data[snack_name] += sale[1]

    if report_data:
        print("Sales Report Data:")
        for snack, quantity in report_data.items():
            print(f"{snack}: {quantity}")

        # Generate a bar chart to visualize sales
        plt.bar(report_data.keys(), report_data.values())
        plt.xlabel('Snack Name')
        plt.ylabel('Quantity Sold')
        plt.title('Sales Report')
        plt.show()
    else:
        print("No sales data to generate a report.")
    notifications.append("Generated sales report")

# Define a function to save notifications to a file
def save_notifications():
    with open("notifications.txt", "w") as f:
        f.write("\n".join(notifications))

# Define a function to load notifications from a file
def load_notifications():
    if os.path.exists("notifications.txt"):
        with open("notifications.txt", "r") as f:
            return f.read().splitlines()
    return []

# Load notifications from a file
notifications = load_notifications()

# Main loop for user interaction
while True:
    user_role = authenticate_user()

    if user_role:
        while True:
            show_menu(user_role)
            choice = input("Enter your choice: ")

            if choice == "1" and user_roles[user_role]["add_snack"]:
                add_snack()
            elif choice == "2" and user_roles[user_role]["remove_snack"]:
                remove_snack()
            elif choice == "3":
                update_availability()
            elif choice == "4":
                record_sale()
            elif choice == "5" and user_roles[user_role]["generate_report"]:
                generate_report()
            elif choice == "6":
                break
            else:
                print("Invalid choice. Please select a valid option.")

        # Save notifications to a file when the user logs out
        save_notifications()
    else:
        print("Authentication failed. Please enter valid credentials.")
