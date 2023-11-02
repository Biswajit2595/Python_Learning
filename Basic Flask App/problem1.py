from flask import Flask
from markupsafe import escape

app=Flask(__name__)
app.debug=True

@app.route("/") 
def hello_world():
    return "Hello World!"

@app.route("/greet/<username>")
def greet(username):
    return 'Hello {}!'.format(escape(username))

@app.route("/farewell/<username>")
def farewell(username):
    return 'Goodbye, {}!'.format(username)

if __name__=='__main__':
    app.run(debug=True)