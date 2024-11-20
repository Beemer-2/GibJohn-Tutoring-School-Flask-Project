import sqlite3


def main():
    
    requests_database = sqlite3.connect("database/requested-teachers.db")
    requests_database_cursor = requests_database.cursor()

    user = input("\n\n\nEnter the username of the user you want to make a teacher (WARNING - CASE SENSITIVE)\n\n\n")

    #print(requests_database_cursor.execute('SELECT * FROM requested').fetchall())
    #print(user)

    for user_tuple in requests_database_cursor.execute("SELECT * FROM requested").fetchall():
        if user in user_tuple:
            #Changes the type of user based on the name entered.
            #Also deletes the user from the requests database.
            main_database = sqlite3.connect("database/main.db")
            main_database_cursor = main_database.cursor()    
            main_database_cursor.execute("UPDATE users SET typeOfUser='teacher' WHERE username=(?)", (user,))
            print("added successfully")
            main_database.commit()
            requests_database_cursor.execute("DELETE FROM requested WHERE username=(?)", (user,))
            requests_database.commit()

            #Deletes the new teacher from the last-working-on database.
            last_working_on_database = sqlite3.connect("database/last-working-on.db")
            last_working_on_database_cursor = last_working_on_database.cursor()  
            last_working_on_database_cursor.execute("DELETE FROM usersLast WHERE username=(?)", (user,))  
            last_working_on_database.commit()
            last_working_on_database.close()
            requests_database.close()
            return


        else:
            pass
            
    print("That user is not in the request database!")
    
    requests_database.close()

def show_all_teachers():
    database = sqlite3.connect("database/main.db")
    database_cursor = database.cursor()

    print(database_cursor.execute("SELECT username, typeOfUser FROM users WHERE typeOfUser='teacher'").fetchall())

    database.close()

main()
show_all_teachers()