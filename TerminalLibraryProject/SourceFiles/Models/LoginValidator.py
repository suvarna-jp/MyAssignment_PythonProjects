# LoginValidator.py
import sqlite3
import sys
from SourceFiles.Commons.CommonIncludes import DEBUG_MODE
from SourceFiles.Commons.CommonIncludes import DB_LOCATION

from SourceFiles.CustomExceptions import IncorrectOptionException

# # Global variable for Debug statements
# DEBUG_MODE = False
# # Global Database file path
# DB_LOCATION = 'C:\\Users\\suvarnajoshi\\PycharmProjects\\TerminalLibraryProject\\DBFiles\\TerminalLibraryDB.db'

def validateUser(cursor, u_id, u_pwd):
    '''Validates the User's login ID and password match connecting to the Database
        @:param cursor - to execute query
        @:param login ID
        @:param password
        @:return list object (1st item of list depicts the execution result
                    1 - Success | 0 - wrong passord | 2 - Unexpected error'''

    if DEBUG_MODE:
        print("Inside validateUser()")

    query = "SELECT * FROM Users WHERE user_RegnNum = '" + str(u_id) + "';"
    cursor.execute(query)
    if DEBUG_MODE:
        print("Executed Query in validateUser()")

    tablelist = cursor.fetchall()
    if ((len(tablelist)) == 1):
        if (tablelist[0][2] == u_pwd):
            if DEBUG_MODE:
                print("Returning :: ", [1, tablelist])
            return [1, tablelist]
        else:
            if DEBUG_MODE:
                print("Returning :: ", [0, None])
            return [0, None]
    else:
        print("Records retrieved not equal to 1. Hence returning :: ", [2, None])
        return [2, None]


def validateLibrarian(cursor, l_id, l_pwd):
    '''Validates the Librarian's login ID and password match connecting to the Database
        @:param cursor - to execute query
        @:param login ID
        @:param password
        @:return list object (1st item of list depicts the execution result
                    1 - Success | 0 - wrong passord | 2 - Unexpected error'''

    if DEBUG_MODE:
        print("Inside validateLibrarian()")

    query = "SELECT * FROM Librarians WHERE librn_RegnNum = '" + str(l_id) + "';"
    cursor.execute(query)
    if DEBUG_MODE:
        print("Executed Query in validateLibrarian()")

    tablelist = cursor.fetchall()
    if DEBUG_MODE:
        print("len(tablelist) :: ", len(tablelist))

    if ((len(tablelist)) == 1):
        if (tablelist[0][2] == l_pwd):
            if DEBUG_MODE:
                print("Returning :: ", [1, tablelist])
            return [1, tablelist]
        else:
            if DEBUG_MODE:
                print("Returning :: ", [0, None])
            return [0, None]
    else:
        print("Records retrieved not equal to 1. Hence returning :: ", [2, None])
        return [2, None]


def isValidUser(user_type, loginID, pwd):
    '''This function establishes connection to Database
    and calls appropriate functions to check the validity
    of login credentials of User/Librarian
    @:param user_type 'U' - User or 'L' - Librarian
    @:param login ID
    @:param password
    @:return list object (1st item of list depicts the execution result'''

    if DEBUG_MODE:
        print("Inside isValidUser()")

    response_validateUser = None
    try:
        connection = sqlite3.connect(DB_LOCATION)
        cursor = connection.cursor()
        if DEBUG_MODE:
            print("Initialized Connection & Cursor")
        try:
            if user_type == 'U':
                if DEBUG_MODE:
                    print("User type is USER")
                response_validateUser = validateUser(cursor, loginID, pwd)
            elif user_type == 'L':
                if DEBUG_MODE:
                    print("User type is LIBRARIAN")
                response_validateUser = validateLibrarian(cursor, loginID, pwd)
            else:
                if DEBUG_MODE:
                    print("Unexpected | Invalid login ID")
                response_validateUser = [99, None]
        except:
            print("Exception Occured in isValidUser while trying to validate user \n", sys.exc_info())
            response_validateUser = [100, ["Validate Exception"]]
    except ConnectionError as ce:
        print("ConnectionError", ce)
        print(ce.__cause__)
        response_validateUser = [100, ["ConnectionError :: ", ce.__cause__]]
    except:
        print("Exception Occured in isValidUser while connecting to DB \n", sys.exc_info())
        response_validateUser = [100, ["ConnectionError :: ", sys.exc_info()]]
    else:
        if(connection):
            cursor.close()
            connection.close()

    if DEBUG_MODE:
        print(response_validateUser)
    return response_validateUser
