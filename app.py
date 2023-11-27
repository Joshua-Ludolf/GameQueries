from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    return render_template("search.html")

if __name__ == "__main__":
    app.run




