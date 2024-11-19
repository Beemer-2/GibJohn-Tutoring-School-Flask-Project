import sqlite3


def main():
    
    requests_database = sqlite3.connect("database/requested-teachers.db")
    requests_database_cursor = requests_database.cursor()

    user = input("\n\n\nEnter the username of the user you want to make a teacher (WARNING - CASE SENSITIVE)\n\n\n")

    print(requests_database_cursor.execute('SELECT * FROM requested').fetchall())
    print(user)

    for user_tuple in requests_database_cursor.execute("SELECT * FROM requested").fetchall():
        if user in user_tuple:
            teachers_database = sqlite3.connect("database/teachers.db")
            teachers_database_cursor = teachers_database.cursor()    
            teachers_database_cursor.execute("INSERT INTO teachers (username) VALUES (?)", (user,))
            print("added successfully")
            teachers_database.commit()

        else:
            print("That user is not in the request database!")

    requests_database.close()

def show_all_teachers():
    database = sqlite3.connect("database/teachers.db")
    database_cursor = database.cursor()

    print(database_cursor.execute("SELECT * FROM teachers").fetchall())

    database.close()


main()