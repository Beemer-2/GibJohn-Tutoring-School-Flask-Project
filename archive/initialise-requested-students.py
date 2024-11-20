import sqlite3

def create_database():
    database = sqlite3.connect("database/students.db")
    db_cursor = database.cursor()
    
    db_cursor.execute("CREATE TABLE students (username VARCHAR UNIQUE)")
    
    database.commit()
    db_cursor.close()
    database.close()



create_database()