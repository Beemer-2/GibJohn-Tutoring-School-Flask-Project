import sqlite3


def main():
    
    requests_database = sqlite3.connect("database/requested-teachers.db")
    requests_database_cursor = requests_database.cursor()

    user = input("\n\n\nEnter the username of the user you want to make a teacher (WARNING - CASE SENSITIVE)\n\n\n")

    print(requests_database_cursor.execute('SELECT * FROM requested').fetchall())
    print(user)

    for user_tuple in requests_database_cursor.execute("SELECT * FROM requested").fetchall():
        if user in user_tuple:
            #change this
            main_database = sqlite3.connect("database/main.db")
            main_database_cursor = main_database.cursor()    
            main_database_cursor.execute("UPDATE users SET typeOfUser='teacher' WHERE username=(?)", (user,))
            print("added successfully")
            main_database.commit()
            requests_database_cursor.execute("DELETE FROM requested WHERE username=(?)", (user,))
            requests_database.commit()

        else:
            print("That user is not in the request database!")

    requests_database.close()

def show_all_teachers():
    database = sqlite3.connect("database/main.db")
    database_cursor = database.cursor()

    print(database_cursor.execute("SELECT * FROM users WHERE typeOfUser='teacher'").fetchall())

    database.close()

main()
show_all_teachers()