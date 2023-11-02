import json
import uuid
from flask import Flask, request, jsonify

app = Flask(__name__)
app.debug = True

# To load data from dictionary
def load_user_data():
    try:
        with open("users.json", "r") as file:
            users = json.load(file)
    except FileNotFoundError:
        users = {}
    return users

def save_user_data(users):
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

users = load_user_data()

@app.route("/")
def Home_page():
    return "Flask app home page"

# CREATE
@app.route("/create", methods=['POST'])
def create():
    data = request.get_json()
    user_id = str(uuid.uuid4())  # auto generation of Unique ID
    new_user = {
        'id': user_id,
        'name': data['name'],
        'email': data['email']
    }
    users[user_id] = new_user
    save_user_data(users)  # Save the user data to the file
    return jsonify({"id": user_id, "user": new_user})

# READ
@app.route("/read", methods=["GET"])
def read():
    return jsonify(users)

@app.route("/read/<string:id>", methods=['GET'])
def get_single(id):
    user = users.get(id)
    if user:
        return jsonify(user)
    return jsonify({"error": "user not found"})

# UPDATE
@app.route("/update/<string:id>", methods=['PUT'])
def update(id):
    user = users.get(id)
    if user:
        data = request.get_json()
        user['name'] = data['name']
        user['email'] = data['email']
        save_user_data(users)  
        return jsonify(user)
    return jsonify({'error': 'user not found'})

# DELETE
@app.route("/delete/<string:id>", methods=["DELETE"])
def delete(id):
    user = users.pop(id, None)
    if user:
        save_user_data(users)  
        return jsonify({'data': "user has been deleted"})
    return jsonify({'error': 'user not found'})

if __name__ == '__main__':
    app.run(debug=True)
