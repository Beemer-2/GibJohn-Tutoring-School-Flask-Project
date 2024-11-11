from flask import Flask, render_template, redirect, url_for, request
import sqlite3
import datetime
import hashlib
    

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
    if request.method == "POST":
        data = request.form
        database = sqlite3.connect("database/main.db")
        db_cursor = database.cursor()
        
        date = datetime.datetime.now()

        email = data.get("email")
        if "@" and "." not in email:
            return "error, invalid email"

        phoneNum = data.get("phoneNum")
        print(phoneNum)
        try:
            int(phoneNum)
        except:
            return "error, invalid phone number"

        current_ID = db_cursor.execute("SELECT ID FROM users WHERE ID=(SELECT max(ID) FROM users)").fetchall()[0][0] + 1


        db_cursor.execute("""INSERT INTO users 
                      (username, password, ID, email, phoneNum, creationDate, lessonsOwned) 
                      VALUES (?,?,?,?,?,?,?)"""
                      , (data.get("username"), hashlib.sha512(data.get("password").encode()).hexdigest(), current_ID, email, phoneNum, date, 0))


        database.commit()
        database.close()

        return "account created with details"

@app.route("/log-in", methods=["POST"])
def log_in_to_account():
    data = request.form
    print(data)
    database = sqlite3.connect("database/main.db")
    
    return "account created with details"


if __name__ == "__main__":
    app.run(debug=True)




