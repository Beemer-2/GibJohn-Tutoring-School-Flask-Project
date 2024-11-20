import sqlite3

def create_database():
    database = sqlite3.connect("database/last-working-on.db")
    db_cursor = database.cursor()
    
    db_cursor.execute("CREATE TABLE usersLast (username VARCHAR UNIQUE, lastWorkingOn VARCHAR)")
    
    database.commit()
    db_cursor.close()
    database.close()



create_database()