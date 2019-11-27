
from flask import Flask

from models import Schema

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/<name>")
def hello_name(name):
    return "Hello " + name

if __name__ == "__main__":
    Schema()
    app.run(debug=True)