from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import datetime
load_dotenv()
app=Flask(__name__)


app.secret_key=os.getenv("SECRET")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class Menu(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),unique=True,nullable=False)
    price=db.Column(db.Integer,nullable=False)
    availability=db.Column(db.Boolean,default=True)
    
class Order(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    items= db.Column(db.String(500), nullable=False)
    total= db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)


with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "Welcome to Zomato"


@app.route("/menu",methods=["GET","POST"])
def menu():
    if request.method=="GET":
        menu_items = Menu.query.all()
        menu=[]
        for item in menu_items:
            dish={
                'id': item.id,
                'name': item.name,
                'price': item.price,
                'availability': item.availability,
            }
            menu.append(dish)
        return jsonify(menu),201
    
    if request.method=="POST":
        data = request.get_json()
        name = data.get('name')
        price = data.get('price')
        availability = data.get('availability')
        if not name or not price or availability is None:
            return jsonify({"error": "Incomplete data. Please provide all the data"}), 400

        # Create a new menu item and store it in the database
        new_item = Menu(name=name, price=price, availability=availability)
        db.session.add(new_item)
        db.session.commit()
        return jsonify({"msg": "New Item added"}), 201

# Routes for Order
@app.route("/order", methods=["GET", "POST"])
def get_order():
    if request.method == "GET":
        orders = Order.query.all()
        order_data = []
        for order in orders:
            item={
                'id': order.id,
                "name" : order.name,
                "items" : order.items,
                "total" : order.total,
                "date" : order.date,
                "status" : order.status
            }
            order_data.append(item)
        return jsonify({"data":order_data})

    if request.method == "POST":
        data = request.get_json()
        items = data['items']
        total = 0
        names=[]
        
        for item in items:
            total += item["price"]
            names.append(item["name"])
            
        item_names=", ".join(names)
        today = datetime.date.today().strftime('%d/%m/%y')
        new_order = Order(name=data['name'], items=item_names, total=total, date=today, status="received")
        db.session.add(new_order)
        db.session.commit()
        return jsonify({"msg": "New order added", "total": total}), 201

# Route for Single Menu Item
@app.route("/menu/<int:id>", methods=["GET", "PATCH", "DELETE"])
def get_single_menu_item(id):
    item=db.session.get(Menu,id)
    if request.method == "GET":
        if item:
            order={
                "id":item.id,
                "name":item.name,
                "price":item.price,
                "availability":item.availability
            }
            return jsonify({"item":order}), 200
        else:
            return jsonify({'error':"Item Not Found"}),404

    if request.method == "PATCH":
        if item:
            data = request.get_json()
            if "name" in data:
                item.name = data["name"]
            if "price" in data:
                item.price = data["price"]
            if "availability" in data:
                item.availability = data["availability"]
            db.session.commit()
            return jsonify({'msg': f'Item with ID:{id} has been updated'}), 200
        else:
            return jsonify({'error': "Item Not Found"}), 404

    if request.method == "DELETE":
        if item:
            db.session.delete(item)
            db.session.commit()
            return jsonify({"msg": f"Item With ID:{id} has been deleted"})
        else:
            return jsonify({'error': "Item Not Found"}), 404

# Route for Single Order
@app.route("/order/<int:id>", methods=["GET", "PATCH", "DELETE"])
def get_single_order(id):
    order = db.session.get(Order,id)
    if request.method == "GET":
        if order:
            details={
                "id":order.id,
                "name":order.name,
                "items":order.items,
                "total":order.total,
                "status":order.status
            }
            return jsonify({'order':details})
        else:
            return jsonify({'msg': f"Order {id} not found"}), 404

    if request.method == "PATCH":
        if order:
            data = request.get_json()
            if "name" in data:
                order.name = data["name"]
            if "items" in data:
                order.items = data["items"]
            if "total" in data:
                order.total = data["total"]
            if "status" in data:
                order.status = data["status"]
            db.session.commit()
            return jsonify({'msg': f'Order {id} has been updated'}), 200
        else:
            return jsonify({'msg': f"Order {id} not found"}), 404

    if request.method == "DELETE":
        if order:
            db.session.delete(order)
            db.session.commit()
            return jsonify({'msg': "order has been deleted"}), 200
        else:
            return jsonify({'msg': f"Order {id} not found"}), 404

@app.route("/order/status/<string:status>")
def get_orderby_status(status):
    orders = Order.query.all()
    order_data = []
    for order in orders:
        if order.status==status:
            item={
                'id': order.id,
                "name" : order.name,
                "items" : order.items,
                "total" : order.total,
                "date" : order.date,
                "status" : order.status
            }
            order_data.append(item)
    return jsonify({"data":order_data}),200



if __name__=='__main__':
    app.run(debug=True)