# AdminOperations.py

import sqlite3
import sys
from SourceFiles.Commons.CommonIncludes import DEBUG_MODE
from SourceFiles.Commons.CommonIncludes import DB_LOCATION

# # Global variable for Debug statements
# DEBUG_MODE = False
# # Global Database file path
# DB_LOCATION = 'C:\\Users\\suvarnajoshi\\PycharmProjects\\TerminalLibraryProject\\DBFiles\\TerminalLibraryDB.db'

def createTableUsers(cursor):
    '''This function 'createTableUsers' creates a table by name 'Users'
        @:param : cursor object'''

    query = 'CREATE TABLE IF NOT EXISTS Users (' \
            '"user_ID" INTEGER PRIMARY KEY AUTOINCREMENT, ' \
            '"user_RegnNum" NUMERIC NOT NULL UNIQUE, ' \
            '"user_Password" TEXT NOT NULL, ' \
            '"user_Name" TEXT NOT NULL, ' \
            '"user_Address" TEXT NOT NULL, ' \
            '"user_EMail" TEXT NOT NULL, ' \
            '"user_Phone" TEXT NOT NULL' \
            ');'

    cursor.execute(query)
    if DEBUG_MODE:
        print("[DEBUG] :: Users Table created!! ")


def createTableLibrarians(cursor):
    '''This function 'createTableLibrarians' creates a table by name 'Librarians'
        @:param : cursor object'''

    query = 'CREATE TABLE IF NOT EXISTS Librarians (' \
            '"librn_ID" INTEGER PRIMARY KEY AUTOINCREMENT, ' \
            '"librn_RegnNum" NUMERIC NOT NULL UNIQUE, ' \
            '"librn_Password" TEXT NOT NULL, ' \
            '"librn_Name" TEXT NOT NULL, ' \
            '"librn_Address" TEXT NOT NULL, ' \
            '"librn_EMail" TEXT NOT NULL, ' \
            '"librn_Phone" TEXT NOT NULL' \
            ');'

    cursor.execute(query)
    if DEBUG_MODE:
        print("[DEBUG] :: Librarians Table created!! ")


def createTableBooks(cursor):
    '''This function 'createTableBooks' creates a table by name 'Books'
        @:param : cursor object'''

    query = 'CREATE TABLE IF NOT EXISTS Books (' \
            '"book_ID" INTEGER PRIMARY KEY AUTOINCREMENT, ' \
            '"book_Code" NUMERIC NOT NULL UNIQUE, ' \
            '"book_Name" TEXT NOT NULL,' \
            '"book_Author" TEXT NOT NULL,' \
            '"book_Publication" TEXT NOT NULL,' \
            '"book_Category" TEXT NOT NULL,' \
            '"book_Fee" REAL NOT NULL,' \
            '"issued_By" NUMERIC REFERENCES Librarians(librn_RegnNum) ON UPDATE NO ACTION ON DELETE NO ACTION,' \
            '"issued_To" NUMERIC UNIQUE REFERENCES Users(user_RegnNum) ON UPDATE NO ACTION ON DELETE NO ACTION,' \
            '"issued_Date" TEXT, ' \
            '"availability_status" TEXT NOT NULL DEFAULT "YES");'

    cursor.execute(query)
    if DEBUG_MODE:
        print("[DEBUG] :: Books Table created!! ")


def createTableBooksRentalTransactionHistory(cursor):
    '''This function 'createTableBooksRentalTransactionHistory'
    creates a table by name 'BooksRentalTransactionHistory'
        @:param : cursor object'''

    query = 'CREATE TABLE IF NOT EXISTS BooksRentalTransactionHistory (' \
            '"tr_ID"	INTEGER PRIMARY KEY AUTOINCREMENT, ' \
            '"book_Code"	NUMERIC NOT NULL, ' \
            '"issued_By"	NUMERIC REFERENCES Librarians(librn_RegnNum) ON UPDATE NO ACTION ON DELETE NO ACTION,' \
            '"issued_To"	NUMERIC UNIQUE REFERENCES Users(user_RegnNum) ON UPDATE NO ACTION ON DELETE NO ACTION,' \
            '"issued_Date"	TEXT NOT NULL, ' \
            '"return_Date"	TEXT NOT NULL, ' \
            '"received_By"	NUMERIC REFERENCES Librarians(librn_RegnNum) ON UPDATE NO ACTION ON DELETE NO ACTION,' \
            '"amount_Paid"	REAL NOT NULL ' \
            ');'

    cursor.execute(query)
    if DEBUG_MODE:
        print("[DEBUG] :: BooksRentalTransactionHistory Table created!! ")


def adminInsertIntoTableUsers(cursor):
    '''This function 'adminInsertIntoTableUsers' populates values into table 'Users'
        @:param : cursor object'''

    rows = 0
    query = 'INSERT INTO Users (user_RegnNum, user_Password, user_Name, user_Address, user_EMail, user_Phone) ' \
            'VALUES ("U000000001", "abcd$", "Reema", "abcd_address", "abcd@email.com", "901-203-5555");'
    cursor.execute(query)
    rows += 1

    query = 'INSERT INTO Users (user_RegnNum, user_Password, user_Name, user_Address, user_EMail, user_Phone) ' \
            'VALUES ("U000000002", "efgh$", "Ronak", "efgh_address", "efgh@email.com", "298-789-8888");'
    cursor.execute(query)
    rows += 1

    query = 'INSERT INTO Users (user_RegnNum, user_Password, user_Name, user_Address, user_EMail, user_Phone) ' \
            'VALUES ("U000000003", "pqrs$", "Srisha", "pqrs_address", "pqrs@email.com", "222-333-4444");'
    cursor.execute(query)
    rows += 1

    query = 'INSERT INTO Users (user_RegnNum, user_Password, user_Name, user_Address, user_EMail, user_Phone) ' \
            'VALUES ("U000000004", "uvw$", "Sam", "uvw_address", "uvw@email.com", "333-666-8888");'
    cursor.execute(query)
    rows += 1

    if DEBUG_MODE:
        print("[DEBUG] :: Number of rows inserted :: ", rows)
        print("[DEBUG] :: Values entered in Users Table!! ")


def adminInsertIntoTableLibrarians(cursor):
    '''This function 'adminInsertIntoTableLibrarians' populates values into table 'Librarians'
        @:param : cursor object'''

    rows = 0
    query = 'INSERT INTO Librarians (librn_RegnNum, librn_Password, librn_Name, librn_Address, librn_EMail, librn_Phone) ' \
            'VALUES ("L000000001", "labcd$", "Phantom", "labcd_address", "labcd@email.com", "901-563-5665");'
    cursor.execute(query)
    rows+=1

    query = 'INSERT INTO Librarians (librn_RegnNum, librn_Password, librn_Name, librn_Address, librn_EMail, librn_Phone) ' \
            'VALUES ("L000000002", "lefgd$", "Spiderman", "lefgd_address", "lefgd@email.com", "444-363-5677");'
    cursor.execute(query)
    rows+=1

    query = 'INSERT INTO Librarians (librn_RegnNum, librn_Password, librn_Name, librn_Address, librn_EMail, librn_Phone) ' \
            'VALUES ("L000000003", "lpqrs$", "Alice", "lpqrs_address", "lpqrs@email.com", "255-676-3456");'
    cursor.execute(query)
    rows+=1

    query = 'INSERT INTO Librarians (librn_RegnNum, librn_Password, librn_Name, librn_Address, librn_EMail, librn_Phone) ' \
            'VALUES ("L000000004", "lghj$", "Elsa", "lghj_address", "lghj@email.com", "787-467-6868");'
    cursor.execute(query)
    rows+=1

    query = 'INSERT INTO Librarians (librn_RegnNum, librn_Password, librn_Name, librn_Address, librn_EMail, librn_Phone) ' \
            'VALUES ("L000000005", "lete$", "Jini", "lete_address", "lete@email.com", "454-455-7898");'
    cursor.execute(query)
    rows+=1

    query = 'INSERT INTO Librarians (librn_RegnNum, librn_Password, librn_Name, librn_Address, librn_EMail, librn_Phone) ' \
            'VALUES ("L000000006", "lklm$", "Radha", "lklm_address", "lklm@email.com", "666-766-7766");'
    cursor.execute(query)
    rows += 1

    if DEBUG_MODE:
        print("[DEBUG] :: Number of rows inserted :: ", rows)
        print("[DEBUG] :: Values entered in Librarians Table!! ")


def adminInsertIntoTableBooks(cursor):
    '''This function 'adminInsertIntoTableBooks' populates values into table 'Books'
        @:param : cursor object'''
    rows = 0
    query = 'INSERT INTO Books (book_Code, book_Name, book_Author, book_Publication, book_Category, book_Fee, issued_By, issued_To, issued_Date, availability_status) ' \
            'VALUES ("B000000001", "The Secret Garden", "Frances", "Charles Baker Classics", "Fairy Tale", 20, "L000000006", "U000000004", "2019-09-04", "NO");'
    cursor.execute(query)
    rows+=1

    query = 'INSERT INTO Books (book_Code, book_Name, book_Author, book_Publication, book_Category, book_Fee, issued_By, issued_To, issued_Date, availability_status) ' \
            'VALUES ("B000000002", "The Puffin Book Of Classic School Stories", "Ruskin Bond", "Penguin Books India", "Fairy Tale", 20, NULL, NULL, NULL, "YES");'
    cursor.execute(query)
    rows+=1

    query = 'INSERT INTO Books (book_Code, book_Name, book_Author, book_Publication, book_Category, book_Fee, issued_By, issued_To, issued_Date, availability_status) ' \
            'VALUES ("B000000003", "Dork Diaries", "Rachel Renee Russel", "Russel Publication", "Documentary", 20, NULL, NULL, NULL, "YES");'
    cursor.execute(query)
    rows+=1

    query = 'INSERT INTO Books (book_Code, book_Name, book_Author, book_Publication, book_Category, book_Fee, issued_By, issued_To, issued_Date, availability_status) ' \
            'VALUES ("B000000004", "Shanghai Secrets", "Jackie Chan", "Dragon Books", "Action", 20, NULL, NULL, NULL, "YES");'
    cursor.execute(query)
    rows+=1

    query = 'INSERT INTO Books (book_Code, book_Name, book_Author, book_Publication, book_Category, book_Fee, issued_By, issued_To, issued_Date, availability_status) ' \
            'VALUES ("B000000005", "The Wimpy Kid", "Ronald Meyer", "Wimpy Classics", "Comedy", 20, "L000000001", "U000000002", "2019-08-15", "NO");'
    cursor.execute(query)
    rows+=1

    query = 'INSERT INTO Books (book_Code, book_Name, book_Author, book_Publication, book_Category, book_Fee, issued_By, issued_To, issued_Date, availability_status) ' \
            'VALUES ("B000000006", "Harry Potter", "J K Rowling", "Harry Potter Classics", "Mystery|Thriller", 20, "L000000002", "U000000001", "2019-07-12", "NO");'
    cursor.execute(query)
    rows+=1

    query = 'INSERT INTO Books (book_Code, book_Name, book_Author, book_Publication, book_Category, book_Fee, issued_By, issued_To, issued_Date, availability_status) ' \
            'VALUES ("B000000007", "The Hobbit", "J R R", "J R R Publications", "Fantasy|Fiction", 20, "L000000003", "U000000003", "2019-08-24", "NO");'
    cursor.execute(query)
    rows += 1

    if DEBUG_MODE:
        print("[DEBUG] :: Number of rows inserted :: ", rows)
        print("[DEBUG] :: Values entered in Books Table!! ")



def performAdminOperationsFirstTime():
    '''This function performs all the required setup functions for the first time app set-up'''

    if DEBUG_MODE:
        print("[DEBUG] :: In performAdminOperationsFirstTime()")

    try:
        # Fetching DB Connection & initializing cursor
        connection = sqlite3.connect(DB_LOCATION)
        cursor = connection.cursor()

        if DEBUG_MODE:
            print("[DEBUG] :: DB connection established, cursor object created.")

        # Creating required tables in DB
        try:
            createTableUsers(cursor)
            createTableLibrarians(cursor)
            createTableBooks(cursor)
            createTableBooksRentalTransactionHistory(cursor)

            if DEBUG_MODE:
                print("[DEBUG] :: Create table queries run successfully. ")
        except:
            print("[EXCEPT] :: Exception occured : In performAdminOperationsFirstTime() while creating tables...")
            print("[EXCEPT] :: ", sys.exc_info())
            if DEBUG_MODE:
                print("[DEBUG] :: Transactions roll back & Closing DB connection")
            connection.rollback()
            connection.close()
            return False
            # Creating required tables in DB
        try:
            adminInsertIntoTableUsers(cursor)
            adminInsertIntoTableLibrarians(cursor)
            adminInsertIntoTableBooks(cursor)

            if DEBUG_MODE:
                print("[DEBUG] :: Tables populated successfylly with random test values")
        except:
            print("[EXCEPT] :: Exception occured : In performAdminOperationsFirstTime() while populating tables...")
            print("[EXCEPT] :: ", sys.exc_info())
            if DEBUG_MODE:
                print("[DEBUG] :: Transactions roll back & Closing DB connection")
            connection.rollback()
            connection.close()
            return False
    except:
        print("[EXCEPT] :: Exception occured : In performAdminOperationsFirstTime()")
        print("[EXCEPT] :: ", sys.exc_info())
        return False
    else:
        if DEBUG_MODE:
            print("[DEBUG] :: Commiting transactions & Closing DB connection")
        connection.commit()
        connection.close()
        return True

