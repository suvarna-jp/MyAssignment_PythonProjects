# CommonOperations.py

import sqlite3
from datetime import date
from datetime import datetime

from SourceFiles.Beans.Book import Book
from SourceFiles.Beans.Librarian import Librarian
from SourceFiles.Beans.User import User
from SourceFiles.Commons.CommonIncludes import DEBUG_MODE
from SourceFiles.Commons.CommonIncludes import DB_LOCATION

# # Global variable for Debug statements
# DEBUG_MODE = False
# # Global Database file path
# DB_LOCATION = 'C:\\Users\\suvarnajoshi\\PycharmProjects\\TerminalLibraryProject\\DBFiles\\TerminalLibraryDB.db'

# Dynamic assignment to prepare the query
# Database table column names
USER_ID_COLUMN = 'user_ID'
LIBRN_ID_COLUMN = 'librn_ID'
BOOK_ID_COLUMN = 'book_ID'

USER_REGN_NUM = 'user_RegnNum'
LIBRN_REGN_NUM = 'librn_RegnNum'
BOOK_CODE = 'book_Code'

USERS_TABLE = 'Users'
LIBRNS_TABLE = 'Librarians'
BOOKS_TABLE = 'Books'
BOOKS_TRNSCN_TABLE = 'BooksRentalTransactionHistory'

USER_COLUMNS = "(user_RegnNum, user_Password, user_Name, user_Address, user_EMail, user_Phone)"
USER_COLUMNS_VALUES = '(?,?,?,?,?,?)'

LIBRN_COLUMNS = "(librn_RegnNum, librn_Password, librn_Name, librn_Address, librn_EMail, librn_Phone)"
LIBRN_COLUMNS_VALUES = '(?,?,?,?,?,?)'

DIGIT_FIELDS_IN_DB = ['book_fee', 'amount_Paid']

def getDBconnection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except ConnectionError as ce:
        print(ce)

    return conn


def getAvailableBooks():
    '''This function fetches the book details (fields that can be shown to a user) from the Books table'''
    if DEBUG_MODE:
        print("Inside getAvailableBooks()")
    availableBooksList = None
    connection = None
    try:
        connection = sqlite3.connect(DB_LOCATION)
        cursor = connection.cursor()
        if DEBUG_MODE:
            print("Initialized Connection & Cursor")

        query = "SELECT book_Code, book_Name, book_Author, book_Publication, book_Category, book_Fee FROM Books WHERE availability_status = 'YES';"
        cursor.execute(query)
        if DEBUG_MODE:
            print("Executed Query in getAvailableBooks()")
        availableBooksList = cursor.fetchall()
        if DEBUG_MODE:
            print("Fetched Books list")
            print("Number of books :: ", len(availableBooksList))
    except sqlite3.Error as error:
        print("Failed to fetch Book details of given book_Code")
        print("sqlite3.Error :: in getBookDetailsForUser()", error)
    finally:
        if (connection):
            connection.close()
            if DEBUG_MODE:
                print("The Sqlite connection is closed")

    if DEBUG_MODE:
        print(availableBooksList)
    return availableBooksList


def getBookDetailsForUser(book_Code:str):
    if DEBUG_MODE:
        print("Inside getBookDetailsForUser()")
    book_details = None

    if book_Code == None or book_Code.strip() == "":
        book_details = [0, None]
        return book_details

    connection = None
    try:
        connection = sqlite3.connect(DB_LOCATION)
        cursor = connection.cursor()
        if DEBUG_MODE:
            print("Initialized Connection & Cursor")

        query = "SELECT book_Code, book_Name, book_Author, book_Publication, book_Category, book_Fee FROM Books WHERE book_Code = '"+ str(book_Code) +"';"
        cursor.execute(query)
        if DEBUG_MODE:
            print("Executed Query in validateUser()")

        book_details = cursor.fetchall()
        if DEBUG_MODE:
            print("Fetched Bookdetails")
            print("Number of books :: ", len(book_details))
        cursor.close()
        book_details = [1, book_details]
    except sqlite3.Error as error:
        print("Failed to fetch Book details of given book_Code")
        print("sqlite3.Error :: in getBookDetailsForUser()", error)
        book_details = [100, error]
    finally:
        if (connection):
            connection.close()
            if DEBUG_MODE:
                print("The Sqlite connection is closed")

    if DEBUG_MODE:
        print(book_details)
    return book_details


def getBookDetailsForLibrarian(book_Code:str):
    if DEBUG_MODE:
        print("[DEBUG] :: Inside getBookDetailsForLibrarian()")
        print("[DEBUG] :: book_Code :: ", book_Code)

    book_details = None

    if (book_Code == None or book_Code.strip() == ""):
        book_details = [0, book_Code]
        return book_details

    connection = None
    try:
        connection = sqlite3.connect(DB_LOCATION)
        cursor = connection.cursor()
        if DEBUG_MODE:
            print("[DEBUG] :: Initialized Connection & Cursor")

        cursor.execute('SELECT * FROM Books WHERE book_Code = "%s";' %book_Code)
        if DEBUG_MODE:
            print("[DEBUG] :: Executed Query in validateUser()")

        response_bookDetails = cursor.fetchall()
        if DEBUG_MODE:
            print("[DEBUG] :: Fetched Bookdetails :: ", book_details)
        cursor.close()
        book_details = [1, response_bookDetails]
    except sqlite3.Error as error:
        if DEBUG_MODE:
            print("[EXCEPT] :: Failed to fetch Book details for the given book_Code")
            print("[EXCEPT] :: sqlite3.Error :: in getBookDetailsForLibrarian()", error)
        book_details = [100, error]
    finally:
        if (connection):
            connection.close()
            if DEBUG_MODE:
                print("[DEBUG] :: The Sqlite connection is closed")

    if DEBUG_MODE:
        print("[DEBUG] :: returning book_details :: ", book_details)
    return book_details


def addBookToBooksTable(book:Book):
    if DEBUG_MODE:
        print("Inside addBookToBooksTable()")
    response_addBookToBooksTable = None
    connection = None
    prev_book_ID = 0
    try:
        connection = sqlite3.connect(DB_LOCATION)
        cursor = connection.cursor()
        if DEBUG_MODE:
            print("Initialized Connection & Cursor")

        query = f'SELECT max({BOOK_ID_COLUMN}) FROM Books;'
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            prev_book_ID = row[0]
            prev_book_ID+=1
        if DEBUG_MODE:
            print("prev_book_ID : ", prev_book_ID)
            print("prev_book_ID_len : ", prev_book_ID.__str__().__len__())

        prev_book_ID_len = prev_book_ID.__str__().__len__()

        book_Code = 'B' + ('0' * (9-prev_book_ID_len)) + str(prev_book_ID)
        if DEBUG_MODE:
            print("Book Code :: ", book_Code)

        book_tuple = (book_Code, book.get_bk_name(), book.get_bk_author(), book.get_bk_publication(), book.get_bk_category(), book.get_bk_fee(), None, None, None, 'YES')

        cursor.execute('INSERT INTO Books (book_Code, book_Name, book_Author, book_Publication, book_Category, '
                 'book_Fee, issued_By, issued_To, issued_Date, availability_status) VALUES (?,?,?,?,?,?,?,?,?,?);', book_tuple)

        connection.commit()
        print("Record inserted successfully into Books table ", cursor.rowcount)
        cursor.close()
        response_addBookToBooksTable = True
    except sqlite3.Error as error:
        print("Failed to insert data into Books table")
        print("sqlite3.Error :: in addBookToBooksTable()", error)
    finally:
        if (connection):
            connection.close()
            if DEBUG_MODE:
                print("The Sqlite connection is closed")

    if DEBUG_MODE:
        print(response_addBookToBooksTable)
    return response_addBookToBooksTable


def deleteBookFromBooksTable(book_Code):
    if DEBUG_MODE:
        print("Inside deleteBookFromBooksTable()")
    response_deleteBook = None
    connection = None
    try:
        connection = sqlite3.connect(DB_LOCATION)
        cursor = connection.cursor()
        if DEBUG_MODE:
            print("Initialized Connection & Cursor")

        query = ('DELETE FROM Books WHERE book_Code = "%s";' %(book_Code))
        cursor.execute(query)
        connection.commit()
        if DEBUG_MODE:
            print("Record deleted successfully from Books table. \nRows Affected :: ", cursor.rowcount)

        response_deleteBook = cursor.rowcount
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to delete data from Books table")
        print("sqlite3.Error :: in deleteBookFromBooksTable()", error)
        response_deleteBook = 100
    finally:
        if (connection):
            connection.close()
            if DEBUG_MODE:
                print("The Sqlite connection is closed")

    if DEBUG_MODE:
        print(response_deleteBook)
    return response_deleteBook


def deleteUserFromUsersTable(user_regn_num:str):
    if DEBUG_MODE:
        print("Inside deleteUserFromUsersTable()")

    response_deleteUser = [0, None]

    if user_regn_num == None and user_regn_num.strip() == "":
        response_deleteUser = 0
        return response_deleteUser

    connection = None
    try:
        connection = sqlite3.connect(DB_LOCATION)
        cursor = connection.cursor()
        if DEBUG_MODE:
            print("Initialized Connection & Cursor")

        query = (f'DELETE FROM {USERS_TABLE} WHERE {USER_REGN_NUM} = "%s";' %(user_regn_num))
        cursor.execute(query)
        connection.commit()
        if DEBUG_MODE:
            print(f"Record deleted successfully from {USERS_TABLE} table. \nRows Affected :: ", cursor.rowcount)

        response_deleteUser = [cursor.rowcount, None]

        cursor.close()
    except sqlite3.Error as error:
        print(f"Failed to delete data from {USERS_TABLE} table")
        print("sqlite3.Error :: in deleteUserFromUsersTable()", error)
        response_deleteUser = [100, error]
    finally:
        if (connection):
            connection.close()
            if DEBUG_MODE:
                print("The Sqlite connection is closed")

    if DEBUG_MODE:
        print(f"[DEBUG] :: response_deleteUser :: {response_deleteUser}")
    return response_deleteUser


def deleteLibrarianFromLibrariansTable(librn_regn_num):
    if DEBUG_MODE:
        print("Inside deleteLibrarianFromLibrariansTable()")
    response_deleteLibrarian = None
    connection = None
    try:
        connection = sqlite3.connect(DB_LOCATION)
        cursor = connection.cursor()
        if DEBUG_MODE:
            print("Initialized Connection & Cursor")

        query = (f'DELETE FROM {LIBRNS_TABLE} WHERE {LIBRN_REGN_NUM} = "%s";' %(librn_regn_num))
        cursor.execute(query)
        connection.commit()
        if DEBUG_MODE:
            print(f"Record deleted successfully from {LIBRNS_TABLE} table. \nRows Affected :: ", cursor.rowcount)

        response_deleteLibrarian = cursor.rowcount
        cursor.close()
    except sqlite3.Error as error:
        print(f"Failed to delete data from {LIBRNS_TABLE} table")
        print("sqlite3.Error :: in deleteLibrarianFromLibrariansTable()", error)
        response_deleteLibrarian = [100, error]
    finally:
        if (connection):
            connection.close()
            if DEBUG_MODE:
                print("The Sqlite connection is closed")

    if DEBUG_MODE:
        print(f"[DEBUG] :: response_deleteLibrarian :: {response_deleteLibrarian}")
    return response_deleteLibrarian


def calcAmntToBePaidAsPerToday(user_regn_num):
    if DEBUG_MODE:
        print("Inside calcAmntToBePaidAsPerToday()")
    response_calcAmount = None
    connection = None
    try:
        connection = sqlite3.connect(DB_LOCATION)
        cursor = connection.cursor()
        if DEBUG_MODE:
            print("Initialized Connection & Cursor")

        query = ('SELECT book_Code, book_Name, book_Fee, issued_Date, issued_To, issued_By FROM Books WHERE issued_To = "%s";' %(user_regn_num))
        cursor.execute(query)
        response_calcAmount = cursor.fetchall()
        if DEBUG_MODE:
            print("Record fetched successfully from Books table.")
            print("response_calcAmount :: ", response_calcAmount)
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to fetch amount data from Books table")
        print("sqlite3.Error :: in calcAmntToBePaidAsPerToday()", error)
    finally:
        if (connection):
            connection.close()
            if DEBUG_MODE:
                print("The Sqlite connection is closed")

    if DEBUG_MODE:
        print(response_calcAmount)
    return response_calcAmount


def UpdateUserDetailsInDB(userRegnNum, usrUpdtList):
    '''This function updates the User info details in the Users table'''

    if DEBUG_MODE:
        print("[DEBUG] :: Inside UpdateUserDetailsInDB()")

    # [Format] :: UPDATE Users SET user_Phone = "222-444-6666" WHERE user_RegnNum = "U000000002";"
    updtQueryStr = "UPDATE Users SET "

    if(userRegnNum == None or userRegnNum.strip() == "" or usrUpdtList == None or len(usrUpdtList) < 1):
        print("[EMPTY] :: Input Variable is null or empty in UpdateUserDetailsInDB() ")
        return False
    else:
        firstEntry = True
        for updateItem in usrUpdtList:
            if firstEntry == False:
                updtQueryStr += ", "

            updtQueryStr += updateItem[0] + " = " + updateItem[1]
            firstEntry = False
        updtQueryStr += " WHERE " + USER_REGN_NUM + " = '" + userRegnNum + "';"

    if DEBUG_MODE:
        print("[DEBUG] :: finally the Update Query string (updtQueryStr) is :: \n", updtQueryStr)

    response_updtUser = None
    connection = None
    try:
        connection = sqlite3.connect(DB_LOCATION)
        cursor = connection.cursor()
        if DEBUG_MODE:
            print("[DEBUG] :: Initialized Connection & Cursor")

        cursor.execute(updtQueryStr)
        connection.commit()

        response_updtUser = cursor.rowcount
        if DEBUG_MODE:
            print("[DEBUG] :: Successfully updated User info in Users table.")
            print("[DEBUG] :: response_updtUser :: ", response_updtUser)
        cursor.close()

    except sqlite3.Error as error:
        print("[EXCEPT] :: Failed to update User info in Users table")
        print("[EXCEPT] :: sqlite3.Error :: in UpdateUserDetailsInDB()", error)
        response_updtUser = 100
    finally:
        if (connection):
            connection.close()
            if DEBUG_MODE:
                print("[DEBUG] :: The Sqlite connection is closed in UpdateUserDetailsInDB()")

    if DEBUG_MODE:
        print("[DEBUG] :: retuning response_updtUser :: ", response_updtUser)
    return response_updtUser


def updateBookInBooksTable(updtBookList):
    '''This function updates the book info details in DB
    @:param book code
    @:param updated book info list'''

    if DEBUG_MODE:
        print("[DEBUG] :: Inside updateBookInBooksTable()")

    updtQueryStr = "UPDATE Books SET "
    nonStringValues = []
    if (updtBookList == None or len(updtBookList) < 1 or updtBookList[1] == None or len(updtBookList[1]) < 1):
        if DEBUG_MODE:
            print("[EMPTY] :: Input Variable is null or empty in updateBookInBooksTable() ")
        return [0, None]
    else:
        firstEntry = True

        if DEBUG_MODE:
            print("[DEBUG] :: updtBookList :: ", updtBookList)
        for updateItem in updtBookList[1]:
            if firstEntry == False:
                updtQueryStr += ", "

            if DEBUG_MODE:
                print(f"[DEBUG] :: updateItem[0] :: {updateItem[0]}")
                print(f"[DEBUG] :: updateItem[1] :: {updateItem[1]}")

            if(updateItem[0] in DIGIT_FIELDS_IN_DB):
                updtQueryStr += updateItem[0] + " = %d "
                nonStringValues.append(updateItem[1])
                if DEBUG_MODE:
                    print(f"[DEBUG] :: nonStringValues appended :: {nonStringValues}")
            else:
                updtQueryStr += updateItem[0] + " = " + updateItem[1]

            firstEntry = False
        updtQueryStr += " WHERE " + BOOK_CODE + " = '" + updtBookList[0] + "';"

    if DEBUG_MODE:
        print("[DEBUG] :: finally the Update Query string (updtQueryStr) is :: \n", updtQueryStr)

    response_updtBook = None
    connection = None
    try:
        connection = sqlite3.connect(DB_LOCATION)
        cursor = connection.cursor()
        if DEBUG_MODE:
            print("[DEBUG] :: Initialized Connection & Cursor")

        if(nonStringValues != None and len(nonStringValues) > 0):
            cursor.execute(updtQueryStr + ", %", (nonStringValues))
        else:
            cursor.execute(updtQueryStr)

        connection.commit()

        response_updtBook = cursor.fetchall()
        if DEBUG_MODE:
            print("[DEBUG] :: Successfully updated Book info in Books table.")
            print("[DEBUG] :: response_updtBook :: ", response_updtBook)
        cursor.close()
        response_updtBook = [1, response_updtBook]
    except sqlite3.Error as error:
        if DEBUG_MODE:
            print("[EXCEPT] :: Failed to update User info in Users table")
            print("[EXCEPT] :: sqlite3.Error :: in updateBookInBooksTable()", error)
        response_updtBook = [100, error]
    finally:
        if (connection):
            connection.close()
            if DEBUG_MODE:
                print("[DEBUG] :: The Sqlite connection is closed in updateBookInBooksTable()")

    if DEBUG_MODE:
        print("[DEBUG] :: retuning response_updtUser :: ", response_updtBook)
    return response_updtBook


def getBookCodesFromBooksTbl():
    '''This function fetches all User Registration IDs from Users table'''
    if DEBUG_MODE:
        print("[DEBUG] :: Inside getBookCodesFromBooksTbl()")

    response_bookCodes = [0, None]
    connection = None
    try:
        connection = sqlite3.connect(DB_LOCATION)
        cursor = connection.cursor()
        if DEBUG_MODE:
            print("[DEBUG] :: Initialized Connection & Cursor")

        query = f"SELECT {BOOK_CODE} FROM Books;"
        cursor.execute(query)

        book_codes = cursor.fetchall()

        if DEBUG_MODE:
            print("[DEBUG] :: book_codes :: ", book_codes)
        cursor.close()

        response_bookCodes = [1, book_codes]
    except sqlite3.Error as error:
        if DEBUG_MODE:
            print("[EXCEPT] :: sqlite3.Error :: in getBookCodesFromBooksTbl()", error)
        response_bookCodes = [100, error]
    finally:
        if (connection):
            connection.close()
            if DEBUG_MODE:
                print("[DEBUG] :: The Sqlite connection is closed in UpdateUserDetailsInDB()")

    if DEBUG_MODE:
        print("[DEBUG] :: retuning response_bookCodes :: ", response_bookCodes)

    return response_bookCodes


def addUserToUsersTable(newUserObj:User):
    '''This function gets the DB connection and inserts new User details to Users table
    On successful insertion, it returns the New User's Registration number & password to show to the user.
    @:param newUserObj:User'''
    if DEBUG_MODE:
        print("[DEBUG] :: Inside addUserToUsersTable()")
        print(f"[DEBUG] :: newUserObj :: {newUserObj}")

    response_addUserToUsersTable = None
    if(newUserObj == None):
        response_addUserToUsersTable = [0, None]
        return response_addUserToUsersTable

    connection = None
    prev_user_ID = 0
    try:
        connection = sqlite3.connect(DB_LOCATION)
        cursor = connection.cursor()
        if DEBUG_MODE:
            print("Initialized Connection & Cursor")

        query = f'SELECT max({USER_ID_COLUMN}) FROM {USERS_TABLE};'
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            prev_user_ID = row[0]
            prev_user_ID+=1
        if DEBUG_MODE:
            print("prev_user_ID : ", prev_user_ID)
            print("prev_user_ID_len : ", prev_user_ID.__str__().__len__())

        prev_user_ID_len = prev_user_ID.__str__().__len__()

        user_regn_num = 'U' + ('0' * (9-prev_user_ID_len)) + str(prev_user_ID)

        user_tuple = (user_regn_num, newUserObj.get_u_pwd(), newUserObj.get_u_name(), newUserObj.get_u_address(), newUserObj.get_u_email(), newUserObj.get_u_phone())

        query = f"INSERT INTO Users {USER_COLUMNS} VALUES {USER_COLUMNS_VALUES};"

        if DEBUG_MODE:
            print("user_regn_num :: ", user_regn_num)
            print("query :: ", query)
            print("user_tuple :: ", user_tuple)

        cursor.execute(query, user_tuple)

        connection.commit()
        print("Record inserted successfully into Users table ", cursor.rowcount)
        response_addUserToUsersTable = [cursor.rowcount, (user_regn_num, newUserObj.get_u_pwd())]
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert data into Users table")
        print("sqlite3.Error :: in addUserToUsersTable()", error)
        response_addUserToUsersTable = [100, error]
    finally:
        if (connection):
            connection.close()
            if DEBUG_MODE:
                print("The Sqlite connection is closed")

    if DEBUG_MODE:
        print(response_addUserToUsersTable)
    return response_addUserToUsersTable

def addLibrarianToLibrariansTable(newLibrarianObj:Librarian):
    '''This function gets the DB connection and inserts new Librarian details to Librarians table
    On successful insertion, it returns the New Librarian's Registration number & password to show to the user.
    @:param newLibrarianObj:User'''
    if DEBUG_MODE:
        print("Inside addLibrarianToLibrariansTable()")

    response_addLibrarian = None
    if(newLibrarianObj == None):
        response_addLibrarian = [0, None]
        return response_addLibrarian

    connection = None
    prev_librn_ID = 0
    try:
        connection = sqlite3.connect(DB_LOCATION)
        cursor = connection.cursor()
        if DEBUG_MODE:
            print("Initialized Connection & Cursor")

        query = f'SELECT max({LIBRN_ID_COLUMN}) FROM {LIBRNS_TABLE};'
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            prev_librn_ID = row[0]
            prev_librn_ID+=1
        if DEBUG_MODE:
            print("prev_librn_ID : ", prev_librn_ID)
            print("prev_librn_ID_len : ", prev_librn_ID.__str__().__len__())

        prev_librn_ID_len = prev_librn_ID.__str__().__len__()

        librn_regn_num = 'L' + ('0' * (9-prev_librn_ID_len)) + str(prev_librn_ID)
        if DEBUG_MODE:
            print("Librarian Registration # :: ", librn_regn_num)

        librn_tuple = (librn_regn_num, newLibrarianObj.get_l_pwd(), newLibrarianObj.get_l_name(),
                       newLibrarianObj.get_l_address(), newLibrarianObj.get_l_email(), newLibrarianObj.get_l_phone())

        cursor.execute(f'INSERT INTO Librarians {LIBRN_COLUMNS} VALUES {LIBRN_COLUMNS_VALUES};', librn_tuple)

        connection.commit()
        print("Record inserted successfully into Librarians table ", cursor.rowcount)
        response_addLibrarian = [cursor.rowcount, (librn_regn_num, newLibrarianObj.get_l_pwd())]
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert data into Librarians table")
        print("sqlite3.Error :: in addLibrarianToLibrariansTable()", error)
        response_addLibrarian = [100, error]
    finally:
        if (connection):
            connection.close()
            if DEBUG_MODE:
                print("The Sqlite connection is closed")

    if DEBUG_MODE:
        print(response_addLibrarian)
    return response_addLibrarian


def updateBookIssued(issueBookTpl):
    '''This function updates the Books table with book issued details
        @:param issueBookTpl - (CURRENT_LIBRARIAN_REGN_ID(issued by), user_regn_num(issued to), book_code)'''

    if DEBUG_MODE:
        print("[DEBUG] :: Inside updateBookIssued()")
        print(f"[DEBUG] :: issueBookTpl :: {issueBookTpl}")
        print(f"[DEBUG] :: date.today() :: {date.today()}")
        print(f"[DEBUG] :: date.today() :: {datetime.today()}")
        print(f"[DEBUG] :: date.today() :: {datetime.now()}")

    if issueBookTpl == None or len(issueBookTpl) != 3:
        if DEBUG_MODE:
            print("[DEBUG] :: issueBookTpl is Null or len(issueBookTpl) != 3 ")
        response_issueBook = [0, None]

    updtQueryStr = f"UPDATE Books SET issued_By=?, issued_To=?, issued_Date='{date.today()}', availability_status='NO' WHERE {BOOK_CODE} = ?;"

    if DEBUG_MODE:
        print("[DEBUG] :: finally the Update Query string (updtQueryStr) is :: \n", updtQueryStr)

    response_issueBook = None
    connection = None
    try:
        connection = sqlite3.connect(DB_LOCATION)
        cursor = connection.cursor()
        if DEBUG_MODE:
            print("[DEBUG] :: Initialized Connection & Cursor")

        cursor.execute(updtQueryStr, issueBookTpl)
        connection.commit()

        response_issueBook = cursor.rowcount
        if DEBUG_MODE:
            print("[DEBUG] :: Successfully updated Book issued details in Books table.")
            print("[DEBUG] :: response_issueBook :: ", response_issueBook)
        cursor.close()
        response_issueBook = [1, response_issueBook]
    except sqlite3.Error as error:
        if DEBUG_MODE:
            print("[EXCEPT] :: Failed to Book issued details in Books table.")
            print("[EXCEPT] :: sqlite3.Error :: in updateBookIssued()", error)
        response_updtLibrarian = [100, error]
    finally:
        if (connection):
            connection.close()
            if DEBUG_MODE:
                print("[DEBUG] :: The Sqlite connection is closed in updateBookIssued()")

    if DEBUG_MODE:
        print("[DEBUG] :: retuning response_issueBook :: ", response_issueBook)
    return response_issueBook


def getAvailablityStatusForABook(book_code):
    '''This function checks the availability status for a book
        @:param book_code'''
    if DEBUG_MODE:
        print("Inside getAvailablityStatusForABook()")

    response_bookAvailabilityStatus = None
    if (book_code == None):
        response_bookAvailabilityStatus = 0
        return response_bookAvailabilityStatus

    connection = None
    try:
        connection = sqlite3.connect(DB_LOCATION)
        cursor = connection.cursor()
        if DEBUG_MODE:
            print("Initialized Connection & Cursor")

        query = f"SELECT availability_status FROM {BOOKS_TABLE} WHERE {BOOK_CODE}='{book_code}';"
        cursor.execute(query)
        response_bookAvailabilityStatus = cursor.fetchall()
        cursor.close()
    except sqlite3.Error as error:
        print(f"Could not fetch availability status data for book code :: {book_code}")
        print("sqlite3.Error :: in addLibrarianToLibrariansTable()", error)
        response_bookAvailabilityStatus = 100
    finally:
        if (connection):
            connection.close()
            if DEBUG_MODE:
                print("The Sqlite connection is closed")

    if DEBUG_MODE:
        print(response_bookAvailabilityStatus)
    return response_bookAvailabilityStatus


def checkIfUserHasABook(user_regn_num):
    '''This function checks the if the user has already been issued a book
        @:param user_regn_num'''
    if DEBUG_MODE:
        print("Inside checkIfUserHasABook()")

    response_userHasABook = None
    if (user_regn_num == None):
        response_userHasABook = 0
        return response_userHasABook

    connection = None
    try:
        connection = sqlite3.connect(DB_LOCATION)
        cursor = connection.cursor()
        if DEBUG_MODE:
            print("Initialized Connection & Cursor")

        query = f"SELECT issued_To, {BOOK_CODE} FROM {BOOKS_TABLE} WHERE issued_To='{user_regn_num}';"
        cursor.execute(query)
        response_userHasABook = cursor.fetchall()
        cursor.close()
    except sqlite3.Error as error:
        print(f"Could not fetch data to check if a book has already been issued to user :: {user_regn_num}")
        print("sqlite3.Error :: in checkIfUserHasABook()", error)
        response_userHasABook = 100
    finally:
        if (connection):
            connection.close()
            if DEBUG_MODE:
                print("The Sqlite connection is closed")

    if DEBUG_MODE:
        print(response_userHasABook)
    return response_userHasABook


def updateBookReturned(bookReturnDetailsTpl):
    '''This function updates the Books table with book return details
            @:param bookReturnDetailsTpl - (CURRENT_LIBRARIAN_REGN_ID(issued by), user_regn_num(issued to), book_code)'''

    #bookReturnDetailsTpl = (book_code, issued_By, issued_To, issued_Date, CURRENT_USER_REGN_ID, total_amount)

    if DEBUG_MODE:
        print("[DEBUG] :: Inside updateBookReturned()")
        print(f"[DEBUG] :: bookReturnDetailsTpl :: {bookReturnDetailsTpl}")

    if bookReturnDetailsTpl == None or len(bookReturnDetailsTpl) != 6:
        if DEBUG_MODE:
            print("[DEBUG] :: bookReturnDetailsTpl is Null or len(bookReturnDetailsTpl) != 6 ")
        response_returnBook = [0, None]
        return response_returnBook

    response_returnBook = None
    connection = None
    try:
        connection = sqlite3.connect(DB_LOCATION)
        cursor = connection.cursor()
        if DEBUG_MODE:
            print("[DEBUG] :: Initialized Connection & Cursor")

        updtQueryStr = f"UPDATE Books SET issued_By=NULL, issued_To=NULL, issued_Date=NULL, " \
                       f"availability_status='YES' WHERE {BOOK_CODE} = '{bookReturnDetailsTpl[0]}';"

        if DEBUG_MODE:
            print("[DEBUG] :: Executed Query string 'updtQueryStr' is :: \n", updtQueryStr)

        cursor.execute(updtQueryStr)

        updtQueryStr = "INSERT INTO BooksRentalTransactionHistory (book_Code, issued_By, " \
                       "issued_To, issued_Date, returned_Date, received_by, amount_Paid) VALUES (" \
                       f"'{bookReturnDetailsTpl[0]}', '{bookReturnDetailsTpl[1]}', '{bookReturnDetailsTpl[2]}', " \
                       f"'{bookReturnDetailsTpl[3]}', '{date.today()}', '{bookReturnDetailsTpl[4]}', " \
                       f"{bookReturnDetailsTpl[5]});"

        if DEBUG_MODE:
            print("[DEBUG] :: Executed Query string 'updtQueryStr' is :: \n", updtQueryStr)

        cursor.execute(updtQueryStr)
        connection.commit()

        response_returnBook = cursor.rowcount
        if DEBUG_MODE:
            print("[DEBUG] :: Successfully updated Book returned details in Books table.")
            print("[DEBUG] :: response_returnBook :: ", response_returnBook)
        cursor.close()
        response_returnBook = [1, response_returnBook]
    except sqlite3.Error as error:
        if DEBUG_MODE:
            print("[EXCEPT] :: Failed to enter Book response_returnBook details in Books table.")
            print("[EXCEPT] :: sqlite3.Error :: in updateBookReturned()", error)
        response_updtLibrarian = [100, error]
    finally:
        if (connection):
            connection.close()
            if DEBUG_MODE:
                print("[DEBUG] :: The Sqlite connection is closed in updateBookReturned()")

    if DEBUG_MODE:
        print("[DEBUG] :: retuning response_returnBook :: ", response_returnBook)
    return response_returnBook


def getUserRegnIDsFromUsersTbl():
    '''This function fetches all User Registration IDs from Users table'''
    if DEBUG_MODE:
        print("[DEBUG] :: Inside getUserRegnIDsFromUsersTbl()")

    response_UserRegnIds = [0, None]
    connection = None
    try:
        connection = sqlite3.connect(DB_LOCATION)
        cursor = connection.cursor()
        if DEBUG_MODE:
            print("[DEBUG] :: Initialized Connection & Cursor")

        query = f"SELECT {USER_REGN_NUM} FROM {USERS_TABLE};"
        cursor.execute(query)

        userRegnIds = cursor.fetchall()

        if DEBUG_MODE:
            print("[DEBUG] :: userRegnIds :: ", userRegnIds)
        cursor.close()

        response_UserRegnIds = [1, userRegnIds]
    except sqlite3.Error as error:
        if DEBUG_MODE:
            print("[EXCEPT] :: sqlite3.Error :: in getUserRegnIDsFromUsersTbl()", error)
        response_UserRegnIds = [100, error]
    finally:
        if (connection):
            connection.close()
            if DEBUG_MODE:
                print("[DEBUG] :: The Sqlite connection is closed in getUserRegnIDsFromUsersTbl()")

    if DEBUG_MODE:
        print("[DEBUG] :: retuning response_UserRegnIds :: ", response_UserRegnIds)

    return response_UserRegnIds


def getUserInfo(userRegnIDforUpdate:str):
    '''This function fetches the User details (fields that can be updated) from the Users table'''
    if DEBUG_MODE:
        print("[DEBUG] :: Inside getUserInfo()")
        print(f"[DEBUG] :: userRegnIDforUpdate :: {userRegnIDforUpdate}")

    if(userRegnIDforUpdate == None or userRegnIDforUpdate.strip() == ""):
        if DEBUG_MODE:
            print("[DEBUG] :: userRegnIDforUpdate is null/empty. Hence reverting back without fetching User info")
        return [0, None]

    user_info = None
    connection = None
    try:
        connection = sqlite3.connect(DB_LOCATION)
        cursor = connection.cursor()
        if DEBUG_MODE:
            print("Initialized Connection & Cursor")

        query = f"SELECT user_ID, user_RegnNum, user_Password, user_Name, user_Address, user_EMail, user_Phone " \
                f"FROM {USERS_TABLE} WHERE user_RegnNum = '{userRegnIDforUpdate}';"

        if DEBUG_MODE:
            print("Executed Query in getUserInfo() :: \n", query)

        cursor.execute(query)

        if DEBUG_MODE:
            print("Executed Query in getUserInfo()")

        user_info = cursor.fetchall()

        if DEBUG_MODE:
            print("Number of records fetched :: ", cursor.rowcount)
            print(f"user_info :: {user_info}")

        user_info = [1, user_info]

    except sqlite3.Error as error:
        print(f"Failed to fetch User details for a given User Registration ID :: {userRegnIDforUpdate}")
        print("sqlite3.Error :: in getUserInfo()", error)
        user_info = [100, error]
    finally:
        if (connection):
            connection.close()
            if DEBUG_MODE:
                print("The Sqlite connection is closed")

    if DEBUG_MODE:
        print(user_info)
    return user_info


def getLibrarianRegnIDsFromLibrariansTbl():
    '''This function fetches all Librarian Registration IDs from Librarian table'''
    if DEBUG_MODE:
        print("[DEBUG] :: Inside getLibrarianRegnIDsFromLibrariansTbl()")

    response_LibrarianRegnIDs = [0, None]
    connection = None
    try:
        connection = sqlite3.connect(DB_LOCATION)
        cursor = connection.cursor()
        if DEBUG_MODE:
            print("[DEBUG] :: Initialized Connection & Cursor")

        query = f"SELECT {LIBRN_REGN_NUM} FROM {LIBRNS_TABLE};"
        cursor.execute(query)

        librnRegnIDs = cursor.fetchall()

        if DEBUG_MODE:
            print("[DEBUG] :: librnRegnIDs :: ", librnRegnIDs)
        cursor.close()

        response_LibrarianRegnIDs = [1, librnRegnIDs]
    except sqlite3.Error as error:
        if DEBUG_MODE:
            print("[EXCEPT] :: sqlite3.Error :: in getLibrarianRegnIDsFromLibrariansTbl()", error)
        response_LibrarianRegnIDs = [100, error]
    finally:
        if (connection):
            connection.close()
            if DEBUG_MODE:
                print("[DEBUG] :: The Sqlite connection is closed in getLibrarianRegnIDsFromLibrariansTbl()")

    if DEBUG_MODE:
        print("[DEBUG] :: retuning response_LibrarianRegnIDs :: ", response_LibrarianRegnIDs)

    return response_LibrarianRegnIDs


def getLibrarianInfo(librnRegnIDforUpdate:str):
    '''This function fetches the Librarian details (fields that can be updated by a Librarian) in the Librarian table'''
    if DEBUG_MODE:
        print("[DEBUG] :: Inside getLibrarianInfo()")
        print(f"[DEBUG] :: librnRegnIDforUpdate :: {librnRegnIDforUpdate}")

    if (librnRegnIDforUpdate == None or librnRegnIDforUpdate.strip() == ""):
        if DEBUG_MODE:
            print("[DEBUG] :: librnRegnIDforUpdate is null/empty. Hence reverting back without fetching Librarian info")
        return [0, None]

    librn_info = None
    connection = None
    try:
        connection = sqlite3.connect(DB_LOCATION)
        cursor = connection.cursor()
        if DEBUG_MODE:
            print("Initialized Connection & Cursor")

        query = f"SELECT librn_ID, librn_RegnNum, librn_Password, librn_Name, librn_Address, librn_EMail, librn_Phone " \
                f"FROM {LIBRNS_TABLE} WHERE {LIBRN_REGN_NUM} = '{librnRegnIDforUpdate}';"

        if DEBUG_MODE:
            print("Executing Query in getLibrarianInfo() :: \n", query)

        cursor.execute(query)
        librn_info = cursor.fetchall()

        if DEBUG_MODE:
            print("Number of records fetched :: ", cursor.rowcount)
            print(f"librn_info :: {librn_info}")

        librn_info = [1, librn_info]

    except sqlite3.Error as error:
        print(f"Failed to fetch Librarian details for a given Librarian Registration ID :: {librnRegnIDforUpdate}")
        print("sqlite3.Error :: in getLibrarianInfo()", error)
        librn_info = [100, error]
    finally:
        if (connection):
            connection.close()
            if DEBUG_MODE:
                print("The Sqlite connection is closed")

    if DEBUG_MODE:
        print(librn_info)
    return librn_info


def updateLibrarianDetailsInDB(librnRegnNum, updtLibrarianList):
    '''This function updates the User info details in the Users table'''

    if DEBUG_MODE:
        print("[DEBUG] :: Inside updateLibrarianDetailsInDB()")

    # [Format] :: UPDATE Librarians SET user_Phone = "222-444-6666" WHERE user_RegnNum = "U000000002";"
    updtQueryStr = f"UPDATE {LIBRNS_TABLE} SET "

    if (librnRegnNum == None or librnRegnNum.strip() == "" or updtLibrarianList == None or len(updtLibrarianList) < 1):
        print("[EMPTY] :: Input Variable is null or empty in updateLibrarianDetailsInDB() ")
        return False
    else:
        firstEntry = True
        for updateItem in updtLibrarianList:
            if firstEntry == False:
                updtQueryStr += ", "

            updtQueryStr += updateItem[0] + " = " + updateItem[1]
            firstEntry = False
        updtQueryStr += " WHERE " + LIBRN_REGN_NUM + " = '" + librnRegnNum + "';"

    if DEBUG_MODE:
        print("[DEBUG] :: finally the Update Query string (updtQueryStr) is :: \n", updtQueryStr)

    response_updtLibrarian = None
    connection = None
    try:
        connection = sqlite3.connect(DB_LOCATION)
        cursor = connection.cursor()
        if DEBUG_MODE:
            print("[DEBUG] :: Initialized Connection & Cursor")

        cursor.execute(updtQueryStr)
        connection.commit()

        response_updtLibrarian = cursor.rowcount
        if DEBUG_MODE:
            print("[DEBUG] :: Successfully updated User info in Users table.")
            print("[DEBUG] :: response_updtLibrarian :: ", response_updtLibrarian)
        cursor.close()

    except sqlite3.Error as error:
        print("[EXCEPT] :: Failed to update User info in Users table")
        print("[EXCEPT] :: sqlite3.Error :: in updateLibrarianDetailsInDB()", error)
        response_updtLibrarian = 100
    finally:
        if (connection):
            connection.close()
            if DEBUG_MODE:
                print("[DEBUG] :: The Sqlite connection is closed in updateLibrarianDetailsInDB()")

    if DEBUG_MODE:
        print("[DEBUG] :: Exiting updateLibrarianDetailsInDB(), retuning response_updtLibrarian :: ", response_updtLibrarian)
    return response_updtLibrarian


