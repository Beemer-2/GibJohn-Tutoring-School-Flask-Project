import sqlite3


#database = sqlite3.connect("database/main.db")
#db_cursor = database.cursor()
#db_cursor.execute("CREATE TABLE users (username VARCHAR UNIQUE, password VARCHAR, ID INT UNIQUE, email VARCHAR, phoneNum INT, creationDate DATETIME, lessonsOwned VARCHAR)")
#database.commit()
#database.close()

database = sqlite3.connect("database/main.db")
db_cursor = database.cursor()

#db_cursor.execute("SELECT ID FROM users WHERE ID=(SELECT max(ID) FROM users);")

import datetime

date = datetime.datetime.now()

db_cursor.execute("""INSERT INTO users 
                  (username, password, ID, email, phoneNum, creationDate, lessonsOwned) 
                  VALUES (?,?,?,?,?,?,?)"""
                 , ("Bob", "thisIsATest", 1, "abc@example.com", 123456789, date, 0))
print(db_cursor.fetchall())
database.commit()
database.close()
#
#

database = sqlite3.connect("database/main.db")
db_cursor = database.cursor()

db_cursor.execute("SELECT * FROM users")

print(db_cursor.fetchall())