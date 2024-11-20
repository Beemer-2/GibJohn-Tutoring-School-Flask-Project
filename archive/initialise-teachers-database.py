import sqlite3

def create_database():
    database = sqlite3.connect("database/teachers.db")
    db_cursor = database.cursor()
    
    db_cursor.execute("CREATE TABLE teachers (username VARCHAR UNIQUE)")
    
    database.commit()
    db_cursor.close()
    database.close()



create_database()