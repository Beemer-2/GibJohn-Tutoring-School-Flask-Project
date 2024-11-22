########################################
##  GibJohn Tutoring Site's Back-end  ##
########################################
##Made for Python version 3.12.4
##Modules needing to be installed are:
##Flask
##Flask-session
##bcrypt


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
    print("username")
    return render_template("home.html", username = session.get("username"))

@app.route("/about")
def about():
    return render_template("about.html", username = session.get("username"))

@app.route("/lessons")
def lessons():
    if session.get("username"):
        return render_template("lessons.html", username = session.get("username"))
    else:
        return render_template("lessons-error.html")

@app.route("/teachers")
def teachers():
    teachers_database = sqlite3.connect("database/main.db")
    teachers_database_cursor = teachers_database.cursor()

    user_teacher_check = teachers_database_cursor.execute("SELECT * FROM users WHERE typeOfUser='teacher' AND username=(?)", (session.get("username"),)).fetchall()
    #Checks to see if the user is logged in at all. If not, it will try to get the value from the tuple in a list returned. It will not be able to get this if there is no user as no tuple will be returned, resulting in an error. This try statement catches this.
    try: 
        user_teacher_check = user_teacher_check[0][0]
    except: 
        teachers_database.close()
        return render_template("teachers-not-logged-in.html", username = session.get("username"))


    if session.get("username") == user_teacher_check:
        
        #Gets all the students and their last worked on course from the main database for use in the "students" part on the teachers' page.
        last_working_on_database = sqlite3.connect("database/last-working-on.db")
        last_working_on_database_cursor = last_working_on_database.cursor()

        all_students_list = last_working_on_database_cursor.execute("SELECT username, lastWorkingOn FROM usersLast").fetchall()

        last_working_on_database_cursor.close()

        teachers_database.close()
        return render_template("teachers.html", username = session.get("username"), students = all_students_list)
    else:
        teachers_database.close()
        return render_template("teachers-not-logged-in.html", username = session.get("username"))


@app.route("/request-access-teachers")
def request_access_teachers():
    requested_teachers_database = sqlite3.connect("database/requested-teachers.db")
    requested_teachers_database_cursor = requested_teachers_database.cursor()

    requested_teachers_database_cursor.execute("INSERT INTO requested (username) VALUES (?)", (session.get("username"),))

    requested_teachers_database.commit()
    requested_teachers_database.close()
    
    return render_template("request-access-teachers.html")




@app.route("/log-in-sign-up-page")
def log_in_sign_up():
    return render_template("log-in-sign-up-page.html", username = session.get("username"))

@app.route("/sign-up", methods=["POST"])
def create_account():
    try:
        data = request.form

        if data.get("username") == "":
            return render_template("invalid-sign-up-username.html")


        #Sets up and opens the database
        database = sqlite3.connect("database/main.db")
        db_cursor = database.cursor()

        date = datetime.datetime.now()

        email = data.get("email")
        #Checks and makes sure there is a "@" and a "." in the email entered
        if "@" and "." not in email:
            return render_template("invalid-email.html")

        #Ensures the number entered is a number and nothing else
        phoneNum = data.get("phoneNum")
        ###print(phoneNum)
        try:
            int(phoneNum)
        except:
            return render_template("invalid-phone-number.html")

        #Gets the last user entered into the database's ID
        current_ID = db_cursor.execute("SELECT ID FROM users WHERE ID=(SELECT max(ID) FROM users);").fetchall()[0][0] + 1
        ###print(current_ID)

        password_len = len(data.get("password"))

        if password_len >= 8:
            pass
        else:
            return render_template("invalid-sign-up-password.html")

        #Generates the salt
        salt = bcrypt.gensalt()
        ###print(salt)

        password = bcrypt.hashpw(data.get("password").encode("utf-8"), salt)

        username = data.get("username")

        #Inserts the entered data into the database as a new user. Generates a hash for the password in the process.
        db_cursor.execute("""INSERT INTO users 
                      (username, password, ID, email, phoneNum, creationDate, lessonsOwned, typeOfUser) 
                      VALUES (?,?,?,?,?,?,?,?)"""
                      , (username, password, current_ID, email, phoneNum, date, 0, "student"))


        #Saves the changes
        database.commit()
        #Closes the database
        db_cursor.close()
        database.close()


        #Sets up a session to keep the user logged-in
        session["username"] = username

        last_working_on_database = sqlite3.connect("database/last-working-on.db")
        last_working_on_database_cursor = last_working_on_database.cursor()
        last_working_on_database_cursor.execute("INSERT INTO usersLast (username, lastWorkingOn) VALUES (?,?)", (username, "N/A"))
        last_working_on_database.commit()
        last_working_on_database.close()


        return render_template("home.html", username = session.get("username"))
    
    except:
        return render_template("unknown-sign-up-error.html")


@app.route("/log-in", methods=["POST"])
def log_in_to_account():
    try:
        data = request.form

        #Loads the database
        database = sqlite3.connect("database/main.db")
        db_cursor = database.cursor()

        username = data.get("log-in-username")

        #Gets the account which matches the username the user is attempting to log in to
        attempted_log_into = db_cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()

        #Checks if the account exists
        if attempted_log_into != []:
            #If it does, get the password and check to see if the password entered and the password stored match
            entered_password = data.get("log-in-password").encode()
            password_stored = db_cursor.execute("SELECT password FROM users WHERE username = ?", (username,)).fetchall()[0][0]

            db_cursor.close()
            database.close()

            #If the passwords match, log the user in
            if bcrypt.checkpw(entered_password, password_stored):
                session["username"] = username
                print(session["username"])
                return render_template("home.html", username = session.get("username"))

            else:
                return render_template("invalid-password.html")

        else:
            db_cursor.close()
            database.close()

            return render_template("invalid-username.html")
    
    except:
        render_template("unknown-log-in-error.html")
    
@app.route("/log-out")
def log_out():
    #Clears the sessions, logging the user out of their account
    print(session.get("username"))
    session.clear()
    return render_template("logged-out.html")

    
    


if __name__ == "__main__":
    app.run(debug=True)

