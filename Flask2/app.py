from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Flask-Bcrypt setup
bcrypt = Bcrypt(app)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(300), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

with app.app_context():
    db.create_all()
    
@app.route('/')
def home():
    return "Welcome to the Advanced Flask App"

@app.route('/register', methods=["GET", "POST"])
def register():
    if 'username' in session:
        return "Already registered user"

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Hash the password using Flask-Bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('profile'))

    return render_template('register.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if 'username' in session:
        return "Already logged in user"

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        stored_user = User.query.filter_by(email=email).first()

        if stored_user and bcrypt.check_password_hash(stored_user.password, password):
            session['username'] = stored_user.username
            return redirect(url_for('profile'))
        else:
            return render_template('login.html', error='Email or password is incorrect!')

    return render_template('login.html')

@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return render_template('login.html')

    existing_user = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_password = request.form['new_password']

        if not all([username, password, new_password]):
            return 'Please fill all the details'

        if not bcrypt.check_password_hash(existing_user.password, password):
            return 'Current password is incorrect!'

        # Hash the new password using Flask-Bcrypt
        hashed_new_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

        existing_user.username = username
        existing_user.password = hashed_new_password

        db.session.commit()
        return ' Profile Updated Successfully'

    return render_template('profile.html', user=existing_user)

@app.route("/logout", methods=['GET'])
def logout():
    session.pop('username', None)
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)

