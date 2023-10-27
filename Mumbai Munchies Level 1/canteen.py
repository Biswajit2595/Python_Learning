# Defining list to keep inventories as dictionaries
snack_inventory=[]

sales_records=[]

# Define a function to add snacks in the inventory List
def add_snack():
    snack_id=input("Enter Snack ID: ")
    snack_name=input("Enter Snack Name: ")
    price=float(input("Enter Snack Price: "))
    available=input("Is the snack available? (yes/no): ").lower()


    snack={
        "id":snack_id,
        "name":snack_name,
        "price":price,
        "available":available == "yes",
    }

    snack_inventory.append(snack)
    print(f"{snack_name} has been added to the inventory.")

# defining a function to remove snack
def remove_snack():
    snack_id=input("Enter Snack ID to remove: ")
    for snack in snack_inventory:
        if snack["id"] == snack_id:
            snack_inventory.remove(snack)
            print(f"Snack with ID {snack_id} has been removed from the inventory.")
            return
        print(f"Snack with ID {snack_id} not found in the inventory.")


# defining a function to check the availability of the snack
def update_availability():
    snack_id=input("Enter Snack ID to update availability: ")
    for snack in snack_inventory:
        if snack["id"] == snack_id:
            available=input("Is the snack available? (yes/no): ").lower()
            snack["available"] = available == "yes"
            print(f"Availability of snack with ID {snack_id} has been updated.")
            return
        print(f"Snack with ID {snack_id} not found in the inventory.")

def record_sale():
    snack_id = input("Enter Snack ID sold: ")
    quantity=int(input("Enter the quantity sold: "))

    for snack in snack_inventory:
        if snack["id"] == snack_id:
            if snack["available"]:
                sales_records.append((snack_id,quantity))
                print(f"Sales of {quantity} {snack['name']} recorded.")
                return
            else:
                print(f"{snack['name']} is not available for sale.")
                return
            
    print(f"Snack with ID {snack_id} not found in the inventory")



# Main loop for user interaction 
while True:
    print("\nCanteen Snack Inventory Management")
    print("1. Add Snack")
    print("2. Remove Snack")
    print("3. Update Snack Availability")
    print("4. Record Sales")
    print("5. Exit")


    choice=input("Enter your choice: ")
# based on the choices the functions will be invoked based on that
    if choice == "1":
        add_snack()
    elif choice == "2":
        remove_snack()
    elif choice == "3":
        update_availability()
    elif choice == "4":
        record_sale()
    elif choice == "5":
        break
    else:
        print("Invalid choice. Please Select a valid option.")

    #Display final inventory and sales records
    print("\n Final Snack Inventory:")
    for snack in snack_inventory:
        print(f"ID: {snack['id']}, Name: {snack['name']},Price: {snack['price']}, Available: {snack['available']}")

    print("\nSales Records:")
    for sale in sales_records:
        snack = next((s for s in snack_inventory if s['id'] == sale[0]),None)
        if snack:
            print(f"Snack: {snack['name']}, Quantity Sold: {sale[1]}")
        else:
            print(f"Snack with ID {sale[0]} not found in the inventory.")