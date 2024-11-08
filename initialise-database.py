import sqlite3

database = sqlite3.connect("database/main.db")
db_cursor = database.cursor()
db_cursor.execute("CREATE TABLE users (username VARCHAR, password VARCHAR, ID INT, email VARCHAR, phoneNum INT, creationDate DATETIME, lessonsOwned VARCHAR)")
database.commit()
database.close()
