########################################
##  GibJohn Tutoring Site's Back-end  ##
########################################

#Imports all necessary modules
from flask import Flask, render_template, redirect, url_for, request, session
from flask_session import Session
import sqlite3
import datetime
import bcrypt
    
#Sets up the application (back-end)
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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

    #Sets up and opens the database
    database = sqlite3.connect("database/main.db")
    db_cursor = database.cursor()
    
    date = datetime.datetime.now()
    
    email = data.get("email")
    #Checks and makes sure there is a "@" and a "." in the email entered
    if "@" and "." not in email:
        return "error, invalid email"
    
    #Ensures the number entered is a number and nothing else
    phoneNum = data.get("phoneNum")
    print(phoneNum)
    try:
        int(phoneNum)
    except:
        return "error, invalid phone number"
    
    current_ID = db_cursor.execute("SELECT ID FROM users WHERE ID=(SELECT max(ID) FROM users);").fetchall()[0][0] + 1
    print(current_ID)

    password_len = len(data.get("password"))

    if password_len >= 8:
        pass
    else:
        return "Password is too short or too long. It needs to be between 8 and 128 characters."

    #Generates the salt
    salt = bcrypt.gensalt()
    print(salt)

    password = bcrypt.hashpw(data.get("password").encode("utf-8"), salt)

    #Inserts the entered data into the database as a new user. Generates a hash for the password in the process.
    db_cursor.execute("""INSERT INTO users 
                  (username, password, ID, email, phoneNum, creationDate, lessonsOwned) 
                  VALUES (?,?,?,?,?,?,?)"""
                  , (data.get("username"), password, current_ID, email, phoneNum, date, 0))


    #Saves the changes
    database.commit()
    #Closes the database
    database.close()

    session["username"] = data.get("username")

    return render_template("templates/index.html", username = session.get("username"))

@app.route("/log-in", methods=["POST"])
def log_in_to_account():
    
    data = request.form
    
    database = sqlite3.connect("database/main.db")
    db_cursor = database.cursor()

    username = data.get("log-in-username")
    
    attempted_log_into = db_cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()

    if attempted_log_into != []:
        entered_password = data.get("log-in-password").encode()
        password_stored = db_cursor.execute("SELECT password FROM users WHERE username = ?", (username,)).fetchall()[0][0]

        if bcrypt.checkpw(entered_password, password_stored):
            return render_template("templates/index.html", username = session.get("username"))
        
        else:
            return "invalid password!"

    else:
        return "invalid"
    



    
    


if __name__ == "__main__":
    app.run(debug=True)

