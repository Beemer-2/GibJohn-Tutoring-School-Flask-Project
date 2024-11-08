from flask import Flask, render_template, redirect, url_for, request
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/log-in-sign-up-page")
def log_in_sign_up():
    return render_template("log-in-sign-up-page.html")

@app.route("/sign-up", methods=["POST"])
def create_account():
    data = request.form
    print(data)
    database = sqlite3.connect("database/main.db")
    
    return "account created with details"

@app.route("/log-in", methods=["POST"])
def log_in_to_account():
    data = request.form
    print(data)
    database = sqlite3.connect("database/main.db")
    
    return "account created with details"


if __name__ == "__main__":
    app.run(debug=True)
