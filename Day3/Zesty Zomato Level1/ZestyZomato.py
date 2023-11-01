import os
import json
import datetime

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

def save_data():
    with open("menu.json", "w") as menu_file:
        json.dump(menu, menu_file, indent=4)
    with open("orders.json", "w") as orders_file:
        json.dump(orders, orders_file, indent=4)

def display_menu():
    print("Menu:")
    for item in menu:
        print(f"{item['dish_id']}: {item['dish_name']} - ₹{item['price']} ({'Available' if item['availability'] else 'Not Available'})")

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
    dish_ids = input("Enter Dish IDs (comma-separated): ").split(',')
    order_id = len(orders) + 1
    order_status = "received"
    today = datetime.date.today()
    order_date = today.strftime("%d/%m/%Y")

    total_price = 0
    for dish_id in dish_ids:
        dish_id = int(dish_id)
        for item in menu:
            if item['dish_id'] == dish_id:
                if item['availability']:
                    total_price += item['price']
                else:
                    print(f"{item['dish_name']} is not available.")
                break
        else:
            print(f"No dish found with ID {dish_id}.")

    if total_price > 0:
        feedback = input("Enter feedback for this order (optional): ")
        order = {
            'order_id': order_id,
            'customer_name': customer_name,
            'dish_ids': dish_ids,
            'order_status': order_status,
            'total_price': total_price,
            'order_date': order_date,
            'feedback': feedback,  # Collect and store feedback here
        }
        orders.append(order)
        save_data()
        print(f"Order {order_id} placed for a total of ₹{total_price}.")
    else:
        print("No valid dishes in the order. Order not placed.")


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

def filter_orders_by_status():
    status = input("Enter status (received/preparing/ready for pickup/delivered): ").lower()
    filtered_orders = [order for order in orders if order['order_status'] == status]
    if filtered_orders:
        print(f"Orders with status '{status}':")
        for order in filtered_orders:
            print(f"Order ID: {order['order_id']}, Customer: {order['customer_name']}, Status: {order['order_status']}")
    else:
        print(f"No orders found with status '{status}'.")

def view_all_feedback():
    feedback_found = False
    for order in orders:
        if 'feedback' in order:
            print(f"Order ID: {order['order_id']}, Feedback: {order['feedback']}")
            feedback_found = True

    if not feedback_found:
        print("No feedback found for any order.")

def daily_sales_summary(date):
    total_sales = 0
    sold=0
    for order in orders:
        if order.get('order_date') == date:
            sold+=1
            total_sales += order['total_price']

    print(f"Sales Summary {sold} orders on {date}: ₹{total_sales}")

def main():
    load_data()
    while True:
        print("\nZesty Zomato: The Great Food Fiasco")
        print("1. Display Menu")
        print("2. Add Dish to Menu")
        print("3. Remove Dish from Menu")
        print("4. Update Dish Availability")
        print("5. Place Order")
        print("6. Update Order Status")
        print("7. Filter Orders by Status")
        print("8. View Feedbacks")
        print("9. Daily Sales Summary")
        print("10. Exit")
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
            filter_orders_by_status()
        elif choice == "8":
            view_all_feedback()
        elif choice == "9":
            date = input("Enter date (DD/MM/YYYY) for sales summary: ")
            daily_sales_summary(date)
        elif choice == "10":
            save_data()
            print("Exiting Zesty Zomato. Have a great day!")
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()
