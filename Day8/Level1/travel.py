from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_planner.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(100), nullable=False)
    # creating relationships
    # itineraries = db.relationship('Itinerary', backref='destination', lazy=True)
    # expenses = db.relationship('Expense', backref='destination', lazy=True)

class Itinerary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(25), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)
    destination = db.relationship('Destination', backref='itineraries')

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))
    description = db.Column(db.String(500))
    date = db.Column(db.String(20))
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)
    destination = db.relationship('Destination', backref='expenses')

with app.app_context():
    db.create_all()

# Routes
@app.route("/")
def home():
    return "Welcome to Wanderlust Travel Planner"

@app.route('/destinations', methods=['GET', 'POST'])
def manage_destinations():
    if request.method == 'GET':
        destinations = Destination.query.all()
        destinations_data = [{"id": dest.id, "name": dest.name, "description": dest.description, "location": dest.location} for dest in destinations]
        return jsonify({"destinations": destinations_data}), 200

    elif request.method == 'POST':
        data = request.json
        new_destination = Destination(
            name=data.get('name'),
            description=data.get('description'),
            location=data.get('location')
        )
        db.session.add(new_destination)
        db.session.commit()
        return jsonify({"message": "Destination created successfully"}), 201

@app.route('/destinations/<int:dest_id>', methods=['GET', 'PUT', 'DELETE', 'PATCH'])
def manage_destination(dest_id):
    destination = Destination.query.get_or_404(dest_id)

    if request.method == 'GET':
        destination_data = {
            "id": destination.id,
            "name": destination.name,
            "description": destination.description,
            "location": destination.location,
            "itineraries": [{"activity": i.activity, "date": str(i.date)} for i in destination.itineraries],
            "expenses": [{"amount": e.amount, "category": e.category, "date": str(e.date)} for e in destination.expenses],
        }
        return jsonify({"destination": destination_data}), 200

    elif request.method == 'PUT':
        data = request.json
        destination.name = data.get('name', destination.name)
        destination.description = data.get('description', destination.description)
        destination.location = data.get('location', destination.location)
        db.session.commit()
        return jsonify({"message": "Destination updated successfully"}), 200

    elif request.method == 'DELETE':
        db.session.delete(destination)
        db.session.commit()
        return jsonify({"message": "Destination deleted successfully"}), 200

    elif request.method == 'PATCH':
        data = request.json
        # Implement patch logic based on your requirements
        # For example, you can update only specific fields
        if 'name' in data:
            destination.name = data['name']
        if 'description' in data:
            destination.description = data['description']
        if 'location' in data:
            destination.location = data['location']
        db.session.commit()
        return jsonify({"message": "Destination patched successfully"}), 200

@app.route('/itineraries', methods=['GET', 'POST'])
def manage_itineraries():
    if request.method == 'GET':
        itineraries = Itinerary.query.all()
        itineraries_data = [{
            "activity": i.activity,
            "date": str(i.date),
            "destination_name": i.destination.name  # Include destination name
        } for i in itineraries]
        return jsonify({"itineraries": itineraries_data}), 200

    elif request.method == 'POST':
        data = request.json
        new_itinerary = Itinerary(
            activity=data.get('activity'),
            date=data.get('date'),
            destination_id=data.get('destination_id')
        )
        db.session.add(new_itinerary)
        db.session.commit()
        return jsonify({"message": "Itinerary created successfully"}), 201

@app.route('/itineraries/<int:itinerary_id>', methods=['GET', 'PUT', 'DELETE', 'PATCH'])
def manage_itinerary(itinerary_id):
    itinerary = Itinerary.query.get_or_404(itinerary_id)

    if request.method == 'GET':
        itinerary_data = {
            "activity": itinerary.activity,
            "date": str(itinerary.date),
            "destination_id": itinerary.destination_id,
            "destination_name": itinerary.destination.name
        }
        return jsonify({"itinerary": itinerary_data}), 200

    elif request.method == 'PUT':
        data = request.json
        itinerary.activity = data.get('activity', itinerary.activity)
        itinerary.date = data.get('date', itinerary.date)
        itinerary.destination_id = data.get('destination_id', itinerary.destination_id)
        db.session.commit()
        return jsonify({"message": "Itinerary updated successfully"}), 200

    elif request.method == 'DELETE':
        db.session.delete(itinerary)
        db.session.commit()
        return jsonify({"message": "Itinerary deleted successfully"}), 200

    elif request.method == 'PATCH':
        data = request.json
        # Implement patch logic based on your requirements
        # For example, you can update only specific fields
        if 'activity' in data:
            itinerary.activity = data['activity']
        if 'date' in data:
            itinerary.date = data['date']
        if 'destination_id' in data:
            itinerary.destination_id = data['destination_id']
        db.session.commit()
        return jsonify({"message": "Itinerary patched successfully"}), 200

@app.route('/expenses', methods=['GET', 'POST'])
def manage_expenses():
    if request.method == 'GET':
        expenses = Expense.query.all()
        expenses_data = [{
            "amount": e.amount,
            "category": e.category,
            "description": e.description,
            "date": str(e.date),
            "destination_name": e.destination.name  # Include destination name
        } for e in expenses]
        return jsonify({"expenses": expenses_data}), 200

    elif request.method == 'POST':
        data = request.json
        new_expense = Expense(
            amount=data.get('amount'),
            category=data.get('category'),
            description=data.get('description'),
            date=data.get('date'),
            destination_id=data.get('destination_id')
        )
        db.session.add(new_expense)
        db.session.commit()
        return jsonify({"message": "Expense created successfully"}), 201

@app.route('/expenses/<int:expense_id>', methods=['GET', 'PUT', 'DELETE', 'PATCH'])
def manage_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)

    if request.method == 'GET':
        expense_data = {
            "amount": expense.amount,
            "category": expense.category,
            "description": expense.description,
            "date": str(expense.date),
            "destination_id": expense.destination_id,
            "destination_name": expense.destination.name
        }
        return jsonify({"expense": expense_data}), 200

    elif request.method == 'PUT':
        data = request.json
        expense.amount = data.get('amount', expense.amount)
        expense.category = data.get('category', expense.category)
        expense.description = data.get('description', expense.description)
        expense.date = data.get('date', expense.date)
        expense.destination_id = data.get('destination_id', expense.destination_id)
        db.session.commit()
        return jsonify({"message": "Expense updated successfully"}), 200

    elif request.method == 'DELETE':
        db.session.delete(expense)
        db.session.commit()
        return jsonify({"message": "Expense deleted successfully"}), 200

    elif request.method == 'PATCH':
        data = request.json
        # Implement patch logic based on your requirements
        # For example, you can update only specific fields
        if 'amount' in data:
            expense.amount = data['amount']
        if 'category' in data:
            expense.category = data['category']
        if 'description' in data:
            expense.description = data['description']
        if 'date' in data:
            expense.date = data['date']
        if 'destination_id' in data:
            expense.destination_id = data['destination_id']
        db.session.commit()
        return jsonify({"message": "Expense patched successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
