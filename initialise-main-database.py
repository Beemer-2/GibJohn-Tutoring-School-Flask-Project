import sqlite3

def create_database():
    database = sqlite3.connect("database/main.db")
    db_cursor = database.cursor()
    db_cursor.execute("CREATE TABLE users (username VARCHAR UNIQUE, password VARCHAR, ID INT UNIQUE, email VARCHAR, phoneNum INT, creationDate DATETIME, lessonsOwned VARCHAR, typeOfUser VARCHAR)")
    database.commit()
    database.close()


def initialise_database():
    database = sqlite3.connect("database/main.db")
    db_cursor = database.cursor()

    db_cursor.execute("SELECT ID FROM users WHERE ID=(SELECT max(ID) FROM users);")

    import datetime
    date = datetime.datetime.now()

    db_cursor.execute("""INSERT INTO users 
                     (username, password, ID, email, phoneNum, creationDate, lessonsOwned, typeOfUser) 
                     VALUES (?,?,?,?,?,?,?,?)"""
                    , ("Bob", "thisIsATest", 1, "abc@example.com", 123456789, date, 0, "student"))
    print(db_cursor.fetchall())
    database.commit()
    database.close()


def select_all():
    database = sqlite3.connect("database/main.db")
    db_cursor = database.cursor()
    db_cursor.execute("SELECT * FROM users")
    print(db_cursor.fetchall())


def lesson_learners_set_up():
    database = sqlite3.connect("database/main.db")
    db_cursor = database.cursor()
    db_cursor.execute("CREATE TABLE lessonOne")
    database.commit()
    database.close()

create_database()
initialise_database()
select_all()