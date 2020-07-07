import sqlite3
import re

pattern = re.compile("[0-9]+") # This is a pattern that is used to check if an id is a valid int

connection = sqlite3.connect("bookDatabase.db") # Creating the database in this example and connecting to it 
cursor = connection.cursor() # Initialising the cursor 

createTable = """ CREATE TABLE IF NOT EXISTS
books(book_id INTEGER PRIMARY KEY, book_Title TEXT, book_Author TEXT, book_Topic TEXT)"""
cursor.execute(createTable) # Creates the table if it doesn't already exist

#----------INSERT---------------------------
def insert(book_Title, book_Author, book_Topic):
    cursor.execute("SELECT * FROM books")
    results = cursor.fetchall()
    if len(results) == 0:
        maxIndex = -1
    else:
        maxIndex = results[-1][0]
    command = 'INSERT INTO books VALUES ({id}, "{title}", "{author}", "{topic}")'.format(id = maxIndex + 1, title = book_Title, author = book_Author, topic = book_Topic)
    cursor.execute(command)

#----------SELECT---------------------------
def showTable(table): # For now this will just be a simple printall type method
    cursor.execute("SELECT * FROM {}".format(table))
    for row in cursor.fetchall():
        #row[0] row[1] row[2] row[3]
        #    id  title author  topic
        print(""" {id}: {title} by {author} ({topic}) """.format(id = row[0], title = row[1], author = row[2], topic = row[3]))
    
#----------UPDATE---------------------------
def update(id, new_Title, new_Author, new_Topic):
    if pattern.match(id):
        id = pattern.findall(id)[0]
        id = int(id)
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        for check_id in books:
            if check_id[0] == id:
                cursor.execute("SELECT * FROM books WHERE book_id = {id}".format(id = id))
                book = cursor.fetchall()[0]
                if new_Title == "":
                    new_Title = book[1]
                if new_Author == "":
                    new_Author = book[2]
                if new_Topic == "":
                    new_Topic = book[3]
                command = """UPDATE books 
                SET book_Title = '{title}',
                book_Author = '{author}',
                book_Topic = '{topic}' 
                WHERE book_id = {id}""".format(title = new_Title, author = new_Author, topic = new_Topic, id = id)
                cursor.execute(command)
    else: print("Invalid id of", id)

#----------DELETE---------------------------
def delete(id):
    if pattern.match(id):
        id = pattern.findall(id)[0]
        id = int(id)
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        for check_id in books:
            if check_id[0] == id:
                command = """DELETE FROM books  
                WHERE book_id = {id}""".format(id = id)
                cursor.execute(command)
    else: print("Invalid id of", id)

#----------COMMIT---------------------------
def commit():
    connection.commit()
    print("Saving changes")

#----------FORCE INSERT---------------------
def forceInsert(id, book_Title, book_Author, book_Topic):
    cursor.execute("SELECT book_id FROM books")
    books = cursor.fetchall()
    for book in books:
        if str(book[0]) == id:
            print("Book",id,"already exists.")
            return
    command = ''' INSERT INTO books
    VALUES ({id}, "{title}", "{author}", "{topic}")
    '''.format(id = id, title = book_Title, author = book_Author, topic = book_Topic)
    cursor.execute(command)
#-------------------------------------------

# Now that the CRUD methods are done, I can work on writting the main loop of this program.

def main():
    print("    My Bookcase")
    showTable("books")
    while(True):
        print('''
        Commands: 
    [1:SELECT] View Bookcase
    [2:INSERT] Add a new book
    [3:UPDATE] Update a book
    [4:DELETE] Delete a book
    [5:COMMIT] Commit Changes
    [FORCE INSERT] Insert a new book into a specific index
    [0:EXIT] Exit
        ''')
        command = input("What would you like to do? ")
        if   command == "1" or command == "SELECT":
            print("[1:SELECT] selected")
            print("\n    My Bookcase")
            showTable("books")
        elif command == "2" or command == "INSERT":
            print("[2:INSERT] selected")
            tempTitle = input("Title: ")
            tempAuthor = input("Author: ")
            tempTopic = input("Topic: ")
            insert(tempTitle, tempAuthor, tempTopic)

        elif command == "3" or command == "UPDATE":
            print("[3:UPDATE] selected")
            tempID = input("ID: ")
            tempTitle = input("Title: ")
            tempAuthor = input("Author: ")
            tempTopic = input("Topic: ")
            update(tempID, tempTitle, tempAuthor, tempTopic)

        elif command == "4" or command == "DELETE":
            print("[4:DELETE] selected")
            tempID = input("ID: ")
            delete(tempID)

        elif command == "5" or command == "COMMIT":
            print("[5:COMMIT] selected")
            commit()

        elif command == "FORCE INSERT":
            print("[FORCE INSERT]")
            tempID = input("ID: ")
            tempTitle = input("Title: ")
            tempAuthor = input("Author: ")
            tempTopic = input("Topic: ")
            forceInsert(tempID, tempTitle, tempAuthor, tempTopic)

        elif command == "0" or command == "EXIT":
            print("[0:EXIT] selected")
            connection.close()
            return

        else:
            print("Unrecognised command:",command)
            print("Please use a number or type the command.\n")

# This is now a somewhat complete program
# The CRUD interaction with the database is complete
# I can:
# Create rows
# Retrieve the Database as a whole
# Update rows
# Delete specific entries
# And even add new rows as specific empty cells to fill gaps

main()