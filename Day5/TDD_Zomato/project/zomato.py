from flask import Flask,jsonify,request
import json
import random
import datetime

app=Flask(__name__)

def load_menu():
    try:
        with open("project/menu.json","r") as file:
            menu=json.load(file)
    except FileNotFoundError:
        menu={}
    return menu

def save_menu(menu):
    with open('project/menu.json',"w") as file:
        json.dump(menu,file,indent=4)
        
menu=load_menu()

def load_orders():
    try:
        with open("project/order.json","r") as file:
            order=json.load(file)
    except FileNotFoundError:
        order={}
    return order

def save_order(order):
    with open('project/order.json',"w") as file:
        json.dump(order,file,indent=4)

order=load_orders()
used_order_ids = set()

@app.route("/")
def home():
    return "Welcome to Zesty Zomato"

def generate_unique_order_id():
    while True:
        unique_id = str(random.randint(100, 999))  # Generate a random 3-digit number
        if unique_id not in used_order_ids:
            return unique_id

@app.route("/menu", methods=["GET", "POST"])
def get_menu():
    if request.method == "GET":
        return jsonify(menu)
    elif request.method == "POST":
        data = request.get_json()
        item=data['name']
        new_item = {
            "name": data["name"],
            "price": data["price"],
            "availability": data["availability"],
        }
        menu[item] = new_item
        save_menu(menu)  # Replace with your save function
        return jsonify({"msg": "New Item added", "item": new_item}), 201

@app.route("/order", methods=["GET", "POST"])
def get_order():
    if request.method == "GET":
        return jsonify(order)
    
    if request.method == "POST":
        data = request.get_json()
        name = data["name"]
        order_items = data.get("items", []) 

        order_id = generate_unique_order_id()

        total = 0
        items_in_order = []
        for order_item in order_items:
            item_name = order_item.get("name")
            item_price = order_item.get("price")
            
            menu_item = next((menu_item for menu_item in menu.values() if menu_item["name"] == item_name), None)
            
            if menu_item:
                item_price = menu_item.get("price", 0)
                total += item_price
                items_in_order.append({"name": item_name, "price": item_price})
        
        date = datetime.date.today()
        order_date = date.strftime("%d/%m/%y")
        
        new_order = {
            "id": order_id,
            "name": name,
            "items": order_items,
            "total": total,
            "date": order_date,
            "status": "received"
        }
        
        order[order_id] = new_order
        used_order_ids.add(order_id)
        save_order(order)  # Replace with your save function
        return jsonify({"msg": "New order added", "total": total}), 201

#Read Single
@app.route("/menu/<string:name>",methods=["GET","PATCH","DELETE"])
def get_single(name):
    if request.method=="GET":
        if name in menu:
            return jsonify({name:menu[name]}),200
        else:
            return jsonify({'error':"Item Not Found"}),404
    if request.method=="PATCH":
        if name in menu:
            data = request.get_json()
            if "name" in data:
                menu[name]["name"] = data["name"]
            if "price" in data:
                menu[name]["price"] = data["price"]
            if "availability" in data:
                menu[name]["availability"] = data["availability"]
            return jsonify({'msg': f'Item {name} updated', 'item': menu[name]}), 200
        else:
            return jsonify({'error': "Item Not Found"}), 404
    if request.method=="DELETE":
        if name in menu:
            del menu[name]
            return jsonify({"msg":f"{name} has been deleted"})
        else:
            return jsonify({'error': "Item Not Found"}), 404

@app.route("/order/<string:id>",methods=["GET","PATCH","DELETE"])
def get_order_single(id):
    if request.method=="GET":
        if id in order:
            return jsonify(order[id]),200
        else:
            return jsonify({'msg':f"Order {id} not found"}),404
    if request.method=="DELETE":
        if id in order:
            del order[id]
            return jsonify({'msg':f"order ID:{id} has been deleted"}),200
        else:
            return jsonify({'msg':f"Order {id} not found"}),404
    if request.method=="PATCH":
        data=request.get_json()
        if id in order:
            if "name" in data:
                order[id]["name"] = data["name"]
            if "items" in data:
                order[id]["items"] = data["items"]
            if "total" in data:
                order[id]["total"] = data["total"]
            if "status" in data:
                order[id]["status"] = data["status"]
            save_order(order)
            return jsonify({'msg': f'Order ID: {id} has been updated'}), 200
        else:
            return jsonify({'msg': f"Order {id} not found"}), 404
    if request.method=="DELETE":
        if id in order:
            del order[id]
            return jsonify({'msg':"order has been deleted"}),200
        else:
            return jsonify({'msg':f"Order {id} not found"}),404


if __name__=='__main__':
    app.run(debug=True)