# LibraryController.py
import datetime
from datetime import datetime
from datetime import date
from datetime import timedelta

from SourceFiles.Views import LoginPageView as lgnVw
from SourceFiles.Views import AdminPageView as admnVw
from SourceFiles.Views import LibrarianPageView as librnVw
from SourceFiles.Views import UserPageView as usrVw
from SourceFiles.Models import LoginValidator as lgnValidator
from SourceFiles.Models import AdminOperations as admnOps
from SourceFiles.Beans import User, Book
from SourceFiles.Beans.Book import Book
from SourceFiles.Beans.User import User
from SourceFiles.Beans.Librarian import Librarian
from SourceFiles.Models import CommonOperations as cOps
from SourceFiles.Commons.CommonIncludes import DEBUG_MODE
from SourceFiles.Commons.CommonIncludes import DB_LOCATION

'''
Some Assumptions made in the project
---------------------------------------------------

Some keywords cannot be used as login ID / Password
Those listed in ['F$P$', 'admin$', 'EXIT$, LOGOUT$']

All users' Registration ID starts with 'U' followed by 9 characters
All librarians' Registration ID starts with 'L' followed by 9 characters

First item of the response list would indicate certain type of responses
Code 1 : Success (or True) # On success, the next item list would hold the successful object/list
Code 0 : Failure (or False)
Code 99 : Invalid entry/value to variable
Code 100 : Exception occured

Terminal messages are grouped into many categories/types.
Some may be enabled only when the DEBUG_MODE is set to true 
They are : 
[WELCOME] - Displays only first time when the user logs in 
[MESSAGE] - Messages displayed to the user 
[INPUT] - When terminal cursor is waiting for the input from user 
[DEBUG] - All debug messages are appended with this. 
            This is enabled only when the DEBUG_MODE is set to true
            These messages would be hidden from the terminal user when DEBUG_MODE is set to false
[EMPTY] - If any expected input/object is null or empty
[ERROR] - If any unexpected error occurs
[EXCEPT] - When an exception occurs (When an exception is caught by the program)
---------------------------------------------------------------------------------------------------------------------
'''

# # Global variable for Debug statements
# DEBUG_MODE = False
# # Global Database file path
# DB_LOCATION = 'C:\\Users\\suvarnajoshi\\PycharmProjects\\TerminalLibraryProject\\DBFiles\\TerminalLibraryDB.db'

# Global variable to identify current use until they logout
# CURRENT_USER can be one in ({'ADMIN':None}|{'USER':<UserObject>}|{'LIBRARIAN':<LibrarianObject>})
CURRENT_USER = None
CURRENT_USER_NAME = None
CURRENT_USER_REGN_ID = None

# Global variable to keep the app running until the end user would like to exit and close the App
# Default value set to True on load of this App
TERMINAL_LIBRARY_APP_RUNNING = True


def interactWithAdmin():
    '''This function iterates through the while loop and keeps calling itself until the admin logs out.
    All the admin related options are put into this code'''

    global CURRENT_USER
    CURRENT_USER = {"ADMIN": None}
    CURRENT_USER_NAME = "ADMIN"

    admin_login = True
    while admin_login:
        admin_option = admnVw.showAdminOptions()
        if (admin_option != None and admin_option.strip() != ""):
            if admin_option == "A":
                admin_ops_response = admnOps.performAdminOperationsFirstTime()
                if (admin_ops_response == True):
                    print("\n[MESSAGE] :: Yo! Sucessfully created tables and populated them.")
                    print("[MESSAGE] :: What would you like to do next?")
                    continue
                else:
                    print("\n[MESSAGE] :: Sorry! Could not perform the admin operations.")
                    print("[MESSAGE] :: Would you like to try options again?")
                    continue
            elif admin_option in ("B", "C", "D"):
                print("\n[MESSAGE] :: Functionalities yet to be implemented.")
                print("[MESSAGE] :: Sorry for the inconvenience!")
                print("[MESSAGE] :: Would you like to try options again?")
                continue
            elif admin_option == "E":
                print("\n[MESSAGE] :: Thank you for using Terminal Library App!")
                print("[MESSAGE] :: Admin : Logging out...")
                admin_login = False
                break
            else:
                print("\n[INVALID] :: Please enter a valid admin option!")
                continue
        else:
            print("\n[EMPTY] :: Null/Empty entry. Please enter a valid admin option!")
            continue

    CURRENT_USER = None
    CURRENT_USER_NAME = None


def interactWithUser(validUser):
    '''This function iterates through the while loop and keeps calling itself until the User logs out.
    All the operations that a User would be allowed to do are called from this function
    @:param User object'''

    if DEBUG_MODE:
        print("[DEBUG] :: In interactWithUser(validUser)")

    global CURRENT_USER
    CURRENT_USER = {'USER': validUser}
    global CURRENT_USER_NAME
    CURRENT_USER_NAME = validUser.get_u_name()
    global CURRENT_USER_REGN_ID
    CURRENT_USER_REGN_ID = validUser.get_u_regn_num()

    if DEBUG_MODE:
        print("[DEBUG] :: CURRENT_USER :: ", CURRENT_USER)
        print("[DEBUG] :: CURRENT_USER_NAME :: ", CURRENT_USER_NAME)
        print("[DEBUG] :: CURRENT_USER_REGN_ID :: ", CURRENT_USER_REGN_ID)

    triggerIfAnyNotificationToUser(CURRENT_USER_REGN_ID)

    userLogin = True
    while userLogin:
        user_option = usrVw.showUserOptions(CURRENT_USER_NAME)
        if DEBUG_MODE:
            print("[DEBUG] :: user_option :: ", user_option)
        return_to_usr = userSelectedOption(user_option)
        if return_to_usr != None and return_to_usr == "LOGOUT$":
            print(f"[MESSAGE] :: User {CURRENT_USER_NAME} Logging out...")
            CURRENT_USER = None
            CURRENT_USER_NAME = None
            userLogin = False
            break

    if DEBUG_MODE:
        print("[DEBUG] :: Exiting interactWithUser()")
    CURRENT_USER = None
    CURRENT_USER_NAME = None


def interactWithLibrarian(validLibrarian):
    '''This function iterates through the while loop and keeps calling itself until the Librarian logs out.
    All the operations that a Librarian would be allowed to do are called from this function
    @:param Librarian object'''

    if DEBUG_MODE:
        print("[DEBUG] :: In interactWithLibrarian")

    global CURRENT_USER, CURRENT_USER_NAME
    CURRENT_USER = {'LIBRARIAN': validLibrarian}
    CURRENT_USER_NAME = validLibrarian.get_l_name()
    global CURRENT_USER_REGN_ID
    CURRENT_USER_REGN_ID = validLibrarian.get_l_regn_num()

    if DEBUG_MODE:
        print("[DEBUG] :: CURRENT_USER :: ", CURRENT_USER)
        print("[DEBUG] :: CURRENT_USER_NAME :: ", CURRENT_USER_NAME)
        print("[DEBUG] :: CURRENT_USER_REGN_ID :: ", CURRENT_USER_REGN_ID)

    librnLogin = True
    while librnLogin:
        librn_option = librnVw.showLibrarianOptions(CURRENT_USER_NAME)
        if DEBUG_MODE:
            print(f"[DEBUG] :: librn_option :: {librn_option}")
        return_to_librn = librarianSelectedOption(librn_option)
        if DEBUG_MODE:
            print(f"[DEBUG] :: return_to_librn :: {return_to_librn}")
        if return_to_librn != None and return_to_librn == "LOGOUT$":
            print(f"[MESSAGE] :: User {CURRENT_USER_NAME} Logging out...")
            CURRENT_USER = None
            CURRENT_USER_NAME = None
            librnLogin = False
            break
        else:
            continue

    if DEBUG_MODE:
        print("[DEBUG] :: Exiting interactWithLibrarian()")
    CURRENT_USER = None
    CURRENT_USER_NAME = None


def viewAvailableBooks():
    '''This function invokes getAvailableBooks() to fetch the list of available books in the library.
    It invokes the showAvailableBooks() by passing the availableBooks list
    to the view, for it to format and display to the user'''

    if DEBUG_MODE:
        print("[DEBUG] :: In viewAvailableBooks()")
    availableBooks = cOps.getAvailableBooks()
    if (availableBooks == None):
        print("[EMPTY] :: Could not fetch available Books!!")
        return False
    elif (len(availableBooks) < 1):
        print("[MESSAGE] :: Sorry! No Books Available at the Library")
        return True
    else:
        librnVw.showAvailableBooks(availableBooks)
        if DEBUG_MODE:
            print("[DEBUG] :: After librnVw.showAvailableBooks(availableBooks) in viewAvailableBooks")
            print("[DEBUG] :: Returning True")
        return True


def viewBookDetails():
    '''This function calls fetchBookCodeFromUser() to fetch book code from the end user
    and calls getBookDetailsForLibrarian() to get the book details '''

    if DEBUG_MODE:
        print("[DEBUG] :: In viewBookDetails()")

    book_Code = librnVw.fetchBookCodeFromUser()
    if (book_Code == None or book_Code.strip() == ""):
        print("[EMPTY] :: Book Code seems to have a Null value. Please try again..")
        viewBookDetails()
    else:
        book = cOps.getBookDetailsForUser(book_Code)
        if DEBUG_MODE:
            print(f"[DEBUG] :: book :: {book}")
        if (book == None or len(book) < 1):
            usrVw.showMessagesToUser(["[EMPTY] :: Unexpected Error Occurred. Please report to Admin."])
            return False
        elif (book[0] == 1 and book[1] is not None and len(book[1]) < 1):
            usrVw.showMessagesToUser([
                "[MESSAGE] :: Sorry! No such Book with book code '" + book_Code + "' exists at the Library"])
            return True
        elif (len(book[1][0]) == 6):
            librnVw.showAvailableBooks(book[1])
            return True
        else:
            usrVw.showMessagesToUser([
                "[ERROR] :: Unexpected Condition :: Found more than 1 record for the same Book_Code. ",
                "\n[ERROR] :: Please report to admin."])
            return False


def addBook():
    '''This function fetches input book details from the view(librarian)
    and adds a book in the database by calling addBookToBooksTable() '''
    newBookObj = librnVw.fetchNewBookDetails(CURRENT_USER_NAME)
    if (newBookObj != None):
        response_addBook = cOps.addBookToBooksTable(newBookObj)
        if response_addBook:
            librnVw.showMessagesToLibrarian(["_______________________________________________________________________",
                                             "[SUCCESS] :: Congratulations! You successfully added a new book "
                                             "to the Library!",
                                             "_______________________________________________________________________"])
            return True
        else:
            librnVw.showMessagesToLibrarian(['[MESSAGE] :: Sorry! Could not add new book. \nPlease try again...'])
            return False
    else:
        librnVw.showMessagesToLibrarian(["[ERROR] :: Unable to read the input you entered."])
        if DEBUG_MODE:
            print("[DEBUG] :: Object is Null")
        return False


def handleErrorsAndExceptions(response_List):
    '''This function handles any errors/exceptions
    deciding what message needs to be shown to the end user
    @:param response_List - [<error code>, <corresponding object>]'''

    if DEBUG_MODE:
        print("[DEBUG] :: in handleErrorsAndExceptions()")

    if (response_List == None or len(response_List) < 1):
        if DEBUG_MODE:
            print("[ERROR] :: response_List is null or empty.")
            print("[ERROR] :: response_List :: ", response_List)
        librnVw.showMessagesToLibrarian(["[ERROR] :: Unhandled Exception occured! Please report to the Admin"])
    elif response_List[0] == 0:
        if DEBUG_MODE:
            print("[ERROR] :: Arguments to the call were null or empty")
            print("[ERROR] :: response_List :: ", response_List)
        librnVw.showMessagesToLibrarian(["[ERROR] :: Exception occured! Please report to the Admin"])
    elif response_List[0] == 100:
        if DEBUG_MODE:
            print("[ERROR] :: Exception occured while interacting with DB")
            print("[ERROR] :: response_List :: ", response_List)
        librnVw.showMessagesToLibrarian(["[ERROR] :: Exception occured! While connection with the databasse. "
                                         "\nPlease report to the Admin"])
    else:
        if DEBUG_MODE:
            print("[ERROR] :: response_List is null or empty.")
            print("[ERROR] :: response_List :: ", response_List)
        librnVw.showMessagesToLibrarian(["[ERROR] :: Unhandled Exception occured! Please report to the Admin"])


def updateBook():
    '''This function invokes fetchBookDetailsForUpdate() that fetches
        the Book deatils from the Librarian and then invokes updateBookInBooksTable()'''

    if DEBUG_MODE:
        print("[DEBUG] :: In updateBook()")

    bookObj: Book = None

    # Reads book code from user/view
    bookCodeforUpdate = librnVw.fetchBookCodeFromUser()
    if DEBUG_MODE:
        print("[DEBUG] :: bookCodeforUpdate :: " + bookCodeforUpdate)
    if bookCodeforUpdate == None or bookCodeforUpdate.strip() == "" or bookCodeforUpdate == "EXIT$":
        return

    # Fetches the entire list of Book codes from the DB
    response_bookCodes = cOps.getBookCodesFromBooksTbl()
    if DEBUG_MODE:
        print(f"[DEBUG] :: response_bookCodes :: {response_bookCodes} ")

    if (response_bookCodes != None and response_bookCodes[0] == 1 and
            response_bookCodes[1] is not None and len(response_bookCodes[1]) > 0):
        for book_code_tpl in response_bookCodes[1]:
            if bookCodeforUpdate not in book_code_tpl:
                print(f"{bookCodeforUpdate} not in {book_code_tpl} \nHence continuing search...")
                continue
            else:
                if DEBUG_MODE:
                    print(f"[DEBUG] :: {bookCodeforUpdate}  found in DB Books list.")
                    print(f"[DEBUG] :: Calling getBookDetailsForLibrarian() by sending {bookCodeforUpdate} ")
                response_bookDetails = cOps.getBookDetailsForLibrarian(bookCodeforUpdate)
                if DEBUG_MODE:
                    print(
                        f"[DEBUG] :: Fetched details for book code :: {bookCodeforUpdate}  :: \n{response_bookDetails}")

                if (response_bookDetails != None and response_bookDetails[0] == 1 and
                        response_bookDetails[1] != None and len(response_bookDetails[1]) == 1):

                    print(f"[DEBUG] :: Checking response_bookDetails[1][0] :: {response_bookDetails[1][0]}")
                    if (response_bookDetails[1][0] != None and len(response_bookDetails[1][0]) == 11):
                        if DEBUG_MODE:
                            print("[DEBUG] :: Assigning the fetched book details to Book object.")

                        bookObj: Book = Book(response_bookDetails[1][0])
                        if (bookObj is not None):
                            updtBookList = librnVw.fetchBookDetailsForUpdate(CURRENT_USER_NAME, bookObj)
                            if (updtBookList != None and type(updtBookList) == str and updtBookList == "EXIT$"):
                                if DEBUG_MODE:
                                    print("[DEBUG] :: updtBookList :: {updtBookList} ")
                                    print("[DEBUG] :: Exiting to Main Menu!")
                                    return
                            elif (updtBookList != None and len(updtBookList) > 0):
                                if DEBUG_MODE:
                                    print(
                                        "[DEBUG] :: Calling updateBookInBooksTable() by Sending updtBookList :: {updateBookInBooksTable} ")

                                response_updateBook = cOps.updateBookInBooksTable(updtBookList)
                                if (response_updateBook != None and response_updateBook[0] == 1):
                                    librnVw.showMessagesToLibrarian(
                                        ["_______________________________________________________________________",
                                         f"[SUCCESS] :: Successfully updated the book details "
                                         f"for Book Code :: {bookCodeforUpdate}",
                                         "_______________________________________________________________________"])
                                    return True
                                else:
                                    handleErrorsAndExceptions(response_updateBook)
                                    return False
                            else:
                                if DEBUG_MODE:
                                    print(f"[EMPTY] :: updtBookList is null/empty :: {updtBookList}")
                                librnVw.showMessagesToLibrarian(
                                    ["[MESSAGE] :: Looks like you did not want to update any field.",
                                     "Hence reverting you back to the Main menu."])
                                return
                        else:
                            if DEBUG_MODE:
                                print("[ERROR] :: Book object could not be initialized.")
                            librnVw.showMessagesToLibrarian([
                                "[ERROR] :: Unexpected error occurred. Please report issue to Admin."])
                            return False
                    elif (response_bookDetails[1][0] != None and response_bookDetails[1][0] == 0):
                        if DEBUG_MODE:
                            print("[DEBUG] :: Zero records fetched from DB")
                        librnVw.showMessagesToLibrarian([
                            f"[INVALID] :: Book details for book code : {bookCodeforUpdate} could not be fetched.",
                            "Please check if you have entered a valid book code and try again.",
                            "Contact Admin if issue still persists."])
                        return
                    else:
                        print(f"[ERROR] :: response_bookDetails[1][0] :: {response_bookDetails[1][0]}")
                        handleErrorsAndExceptions(response_bookDetails)
                else:
                    handleErrorsAndExceptions(response_bookDetails)
                    return False
        else:
            if DEBUG_MODE:
                print(f"[DEBUG] :: {bookCodeforUpdate} doesn't exist in the Library.")
            librnVw.showMessagesToLibrarian([
                "[INVALID] :: This book code doesn't exist in our Terminal Library System",
                "[MESSAGE] :: Please check the list of all books in Library and enter valid Book Code."])
            return
    else:
        handleErrorsAndExceptions(response_bookCodes)
        return False


def deleteBook():
    '''This function invokes fetchBookCodeToDeleteBook() that fetches
    the Book Code from the Librarian and then invokes deleteBookFromBooksTable()'''
    if DEBUG_MODE:
        print("[DEBUG] :: In deleteBook()")

    book_Code = librnVw.fetchBookCodeToDeleteBook(CURRENT_USER_NAME)
    if (book_Code == None or book_Code == False):
        if DEBUG_MODE:
            print("[DEBUG] :: Reverting librarian to the main menu")
        librnVw.showMessagesToLibrarian([f"[MESSAGE] :: Reverting back to the main menu"])
        return False
    else:
        response_bookDelete = cOps.deleteBookFromBooksTable(book_Code)
        if (response_bookDelete != None and response_bookDelete == 1):
            librnVw.showMessagesToLibrarian(["_______________________________________________________________________",
                                             f"[SUCCESS] :: Successfully deleted the book (book code : {book_Code})",
                                             "_______________________________________________________________________"])
            return True
        else:
            librnVw.showMessagesToLibrarian(["[ERROR] :: Could not delete book. "
                                             "Please contact Admin if the problem persists."])
            return False


def addUser():
    '''This function adds a new User by creating a new User account
    and fetches back the new User's Registration Number to display in response to adding new User'''
    if DEBUG_MODE:
        print("[DEBUG] :: In addUser()")
    newUserObj = librnVw.fetchNewUserDetails(CURRENT_USER_NAME)
    if (newUserObj != None):
        if DEBUG_MODE:
            print(f"[DEBUG] :: newUserObj :: {newUserObj}")
        if type(newUserObj) == str and newUserObj == "EXIT$":
            return
        response_addUser = cOps.addUserToUsersTable(newUserObj)
        if DEBUG_MODE:
            print(f"[DEBUG] :: response_addUser :: {response_addUser}")
        if response_addUser == None:
            if DEBUG_MODE:
                print(f"[DEBUG] :: response_addUser :: {response_addUser}")
            librnVw.showMessagesToLibrarian(["[ERROR] :: Unexpected error occurred. Please report to admin."])
        elif response_addUser[0] == 1 and response_addUser[1] is not None and len(response_addUser[1]) == 2:
            librnVw.showMessagesToLibrarian(
                ["\n_______________________________________________________________________",
                 "[SUCCESS] :: Successfully added new User to the Terminal Library App",
                 "The new User's login credentials are :: ",
                 f"\n\tUser's Registration ID :: {response_addUser[1][0]}",
                 f"\tUser's Password :: {response_addUser[1][1]}",
                 "_______________________________________________________________________\n"])
            return True
        else:
            if DEBUG_MODE:
                print(f"[ERROR] :: response_addUser :: {response_addUser}")
            handleErrorsAndExceptions(response_addUser)
            return False
    else:
        librnVw.showMessagesToLibrarian(["[ERROR] :: Unable to read the input you entered. "
                                         "Please try again or report to Admin"])
        if DEBUG_MODE:
            print("[DEBUG] :: newUserObj is Null")
        return False


def updateUser():
    '''This function invokes fetchUserDetailsForUpdate() that fetches
            the User details from the Librarian and then invokes updateUserInUsersTable()'''

    if DEBUG_MODE:
        print("[DEBUG] :: In updateUser()")

    userObj: User = None

    # Reads User Registration ID from view
    userRegnIDforUpdate = librnVw.fetchUserRegnNum(CURRENT_USER_NAME)
    if DEBUG_MODE:
        print("[DEBUG] :: userRegnIDforUpdate :: " + userRegnIDforUpdate)
    if userRegnIDforUpdate == None or userRegnIDforUpdate.strip() == "" or userRegnIDforUpdate == "EXIT$":
        if DEBUG_MODE:
            print("[DEBUG] :: userRegnIDforUpdate is Null/Empty or user chose EXIT$ " + userRegnIDforUpdate)
        return

    # Fetches the entire list of User Registration IDs from the DB
    response_UserRegnIDs = cOps.getUserRegnIDsFromUsersTbl()
    if DEBUG_MODE:
        print(f"[DEBUG] :: response_UserRegnIDs :: {response_UserRegnIDs} ")

    if (response_UserRegnIDs != None and len(response_UserRegnIDs) > 0 and response_UserRegnIDs[0] == 1 and
            response_UserRegnIDs[1] is not None and len(response_UserRegnIDs[1]) > 0):
        for userRegnID_tpl in response_UserRegnIDs[1]:
            if userRegnIDforUpdate not in userRegnID_tpl:
                print(f"{userRegnIDforUpdate} not in {userRegnID_tpl} \nHence continuing search...")
                continue
            else:
                if DEBUG_MODE:
                    print(f"[DEBUG] :: {userRegnIDforUpdate}  found in DB User Registration IDs' list.")
                    print(f"[DEBUG] :: Calling getUserInfo() by sending {userRegnIDforUpdate} ")
                response_UserInfo = cOps.getUserInfo(userRegnIDforUpdate)
                if DEBUG_MODE:
                    print(
                        f"[DEBUG] :: Fetched User details for User Registration ID :: {userRegnIDforUpdate}  :: "
                        f"\n{response_UserInfo}")

                if (response_UserInfo != None and response_UserInfo[0] == 1 and
                        response_UserInfo[1] != None and len(response_UserInfo[1]) == 1):

                    print(f"[DEBUG] :: Checking response_UserInfo[1][0] :: {response_UserInfo[1][0]}")
                    if (response_UserInfo[1][0] != None and len(response_UserInfo[1][0]) == 7):
                        if DEBUG_MODE:
                            print("[DEBUG] :: Assigning the fetched User Info to User object.")

                        userObj = User(response_UserInfo[1][0])
                        if (userObj is not None):
                            updtUserList = librnVw.fetchUserUpdateDetails(CURRENT_USER_NAME, userObj)
                            if (updtUserList != None and type(updtUserList) == str and updtUserList == "EXIT$"):
                                if DEBUG_MODE:
                                    print(
                                        "[DEBUG] :: Looks like user chose to EXIT$ :: updtUserList :: {updtUserList} ")
                                    print("[DEBUG] :: Hence exiting to Main Menu!")
                                    return
                            elif (updtUserList != None and len(updtUserList) > 0):
                                if DEBUG_MODE:
                                    print(f"[DEBUG] :: Calling updateUserInUsersTable() by Sending updtUserList :: "
                                          f"{updtUserList} ")

                                response_updateUser = cOps.UpdateUserDetailsInDB(userObj.get_u_regn_num(), updtUserList)
                                if DEBUG_MODE:
                                    print(f"[DEBUG] :: response_updateUser :: {response_updateUser}")
                                if (response_updateUser != None and response_updateUser == 1):
                                    librnVw.showMessagesToLibrarian(
                                        ["\n_______________________________________________________________________",
                                         f"[SUCCESS] :: Successfully updated the User details "
                                         f"for User Registration ID :: {userRegnIDforUpdate}",
                                         "_______________________________________________________________________"])
                                    return True
                                else:
                                    librnVw.showMessagesToLibrarian(
                                        [f"[ERROR] :: Could not update the User details "
                                         f"Please contact the admin if problem persists."])
                                    return False
                            else:
                                if DEBUG_MODE:
                                    print(f"[EMPTY] :: updtUserList is null/empty :: {updtUserList}")
                                librnVw.showMessagesToLibrarian(
                                    ["[MESSAGE] :: Looks like you did not want to update any field.",
                                     "Hence reverting you back to the Main menu."])
                                return
                        else:
                            if DEBUG_MODE:
                                print("[ERROR] :: User object could not be initialized.")
                            librnVw.showMessagesToLibrarian([
                                "[ERROR] :: Unexpected error occurred. Please report issue to Admin."])
                            return False
                    elif (response_UserInfo[1][0] != None and response_UserInfo[1][0] == 0):
                        if DEBUG_MODE:
                            print("[DEBUG] :: Zero records fetched from DB")
                        librnVw.showMessagesToLibrarian([
                            f"[INVALID] :: User Info for User Registration ID : {userRegnIDforUpdate} could not be fetched.",
                            "Please check if you have entered a valid User Registration ID and try again.",
                            "Contact Admin if issue still persists."])
                        return
                    else:
                        print(f"[ERROR] :: response_UserInfo[1][0] :: {response_UserInfo[1][0]}")
                        handleErrorsAndExceptions(response_UserInfo)
                else:
                    handleErrorsAndExceptions(response_UserInfo)
                    return False
        else:
            if DEBUG_MODE:
                print(f"[DEBUG] :: {userRegnIDforUpdate} doesn't exist in the Library.")
            librnVw.showMessagesToLibrarian([
                "[INVALID] :: This User Registration ID doesn't exist in our Terminal Library System",
                "[MESSAGE] :: Please check once again and enter valid User Registration ID."])
            return
    else:
        handleErrorsAndExceptions(userRegnIDforUpdate)
        return False


def deleteUser():
    '''This function invokes fetchUserRegnNumToDeleteUser() that fetches
        the User Registration Number from the Librarian and then invokes deleteUserFromUsersTable()'''

    if DEBUG_MODE:
        print(f"[DEBUG] :: In deleteUser()")

    user_regn_num = librnVw.fetchUserRegnNumToDeleteUser(CURRENT_USER_NAME)
    if DEBUG_MODE:
        print(f"[DEBUG] :: user_regn_num :: {user_regn_num}")

    if (user_regn_num == None or user_regn_num == False):
        if DEBUG_MODE:
            print("[DEBUG] :: Reverting librarian to the Main menu")
        librnVw.showMessagesToLibrarian(["[EMPTY] :: Could not read registration number. "
                                         "Please contact admin if the problem persists."])
        return False
    elif user_regn_num == 'EXIT$':
        if DEBUG_MODE:
            print("[DEBUG] :: librarian chose to exit to the Main menu")
        return
    else:
        if DEBUG_MODE:
            print("[DEBUG] :: Calling deleteUserFromUsersTable() by passing user_regn_num :: ", user_regn_num)

        response_UserDelete = cOps.deleteUserFromUsersTable(user_regn_num)
        if DEBUG_MODE:
            print(f"[DEBUG] :: response_UserDelete :: {response_UserDelete}")

        if (response_UserDelete == None):
            librnVw.showMessagesToLibrarian(["[ERROR] :: Unexpected error occured. "
                                             "Please contact admin if the problem persists."])
        elif response_UserDelete[0] == 1:
            librnVw.showMessagesToLibrarian(
                ["\n_______________________________________________________________________",
                 "[SUCCESS] :: Successfully deleted the User's record for ",
                 f"User Registration Number :: {user_regn_num}",
                 "_______________________________________________________________________"])
        else:
            handleErrorsAndExceptions(response_UserDelete)
        return True


def deleteLibrarian():
    '''This function invokes fetchLibrarianRegnNumToDeleteLibrarian() that fetches
        the User Registration Number from the Librarian and then invokes deleteLibrarianFromLibrariansTable()'''

    if DEBUG_MODE:
        print("[DEBUG] :: In deleteLibrarian()")

    current_librn_obj: Librarian = CURRENT_USER.get('LIBRARIAN')
    current_librn_regn_num = current_librn_obj.get_l_regn_num()

    if DEBUG_MODE:
        print(f"[DEBUG] :: current_librn_obj :: {current_librn_obj}")
        print(f"[DEBUG] :: current_librn_regn_num :: {current_librn_regn_num}")

    librn_regn_num = librnVw.fetchLibrarianRegnNumToDeleteLibrarian(CURRENT_USER_NAME)
    if DEBUG_MODE:
        print(f"[DEBUG] :: librn_regn_num :: {librn_regn_num}")

    if (librn_regn_num == None or librn_regn_num == False):
        if DEBUG_MODE:
            print("[DEBUG] :: Reverting librarian to the Main menu")
        librnVw.showMessagesToLibrarian(["[EMPTY] :: Could not read registration number. "
                                         "Please contact admin if the problem persists."])
        return False
    elif librn_regn_num == 'EXIT$':
        if DEBUG_MODE:
            print("[DEBUG] :: librarian chose to exit to the Main menu")
        return
    elif librn_regn_num == current_librn_regn_num:
        librnVw.showMessagesToLibrarian([
            "[WARNING] :: Sorry! You cannot choose to delete your own account! :-)",
            "[MESSAGE] :: Redirecting to the Main menu"])
        return
    else:
        if DEBUG_MODE:
            print("[DEBUG] :: Calling deleteLibrarianFromLibrariansTable() by passing librn_regn_num :: ",
                  librn_regn_num)

        response_librarianDelete = cOps.deleteLibrarianFromLibrariansTable(librn_regn_num)
        if DEBUG_MODE:
            print(f"[DEBUG] :: response_librarianDelete :: {response_librarianDelete}")

        if (response_librarianDelete != None) and type(
                response_librarianDelete) == int and response_librarianDelete == 1:
            librnVw.showMessagesToLibrarian(
                ["\n_______________________________________________________________________",
                 "[SUCCESS] :: Successfully deleted the Librarian's record for ",
                 f"Librarian Registration Number :: {librn_regn_num}",
                 "_______________________________________________________________________"])
        else:
            librnVw.showMessagesToLibrarian(["[ERROR] :: Unexpected error occured. "
                                             "Please contact admin if the problem persists."])
        return True


def addLibrarian():
    '''This function adds a new Librarian by creating a new Librarian account
    and fetches back the new Librarian's Registration Number to display in response to adding new Librarian'''

    if DEBUG_MODE:
        print("[DEBUG] :: In addLibrarian()")

    newLibrarianObj = librnVw.fetchNewLibrarianDetails(CURRENT_USER_NAME)
    if DEBUG_MODE:
        print(f"[DEBUG] :: newLibrarianObj :: {newLibrarianObj}")

    if (newLibrarianObj != None):
        if type(newLibrarianObj) == str and newLibrarianObj == "EXIT$":
            return
        response_addLibrarian = cOps.addLibrarianToLibrariansTable(newLibrarianObj)
        if DEBUG_MODE:
            print(f"[DEBUG] :: response_addLibrarian :: {response_addLibrarian}")
        if response_addLibrarian == None:
            if DEBUG_MODE:
                print(f"[DEBUG] :: response_addLibrarian :: {response_addLibrarian}")
            librnVw.showMessagesToLibrarian(["[ERROR] :: Unexpected error occurred. Please report to admin."])
        elif response_addLibrarian[0] == 1 and response_addLibrarian[1] is not None and len(
                response_addLibrarian[1]) == 2:
            librnVw.showMessagesToLibrarian(
                ["\n_______________________________________________________________________",
                 "[SUCCESS] :: Successfully added new Librarian to the Terminal Library App",
                 "The new Librarian's login credentials are :: ",
                 f"\n\tLibrarian's Registration ID :: {response_addLibrarian[1][0]}",
                 f"\tLibrarian's Password :: {response_addLibrarian[1][1]}",
                 "\n_______________________________________________________________________\n"])
            return True
        else:
            if DEBUG_MODE:
                print(f"[ERROR] :: response_addLibrarian :: {response_addLibrarian}")
            handleErrorsAndExceptions(response_addLibrarian)
            return False
    else:
        librnVw.showMessagesToLibrarian(["[ERROR] :: Unable to read the input you entered. "
                                         "Please try again or report to Admin"])
        if DEBUG_MODE:
            print("[DEBUG] :: newLibrarianObj is Null")
        return False


def updateLibrarian():
    '''This function invokes fetchLibrarianDetailsForUpdate() that fetches
                the Librarian details from the Librarian and then invokes updateLibrarianInLibrariansTable()'''

    if DEBUG_MODE:
        print("[DEBUG] :: In updateLibrarian()")

    librnObj: Librarian = None

    # Reads Librarian Registration Number from Librarian/view
    librnRegnIDforUpdate = librnVw.fetchLibrarianRegnNum(CURRENT_USER_NAME)
    if DEBUG_MODE:
        print("[DEBUG] :: librnRegnIDforUpdate :: " + librnRegnIDforUpdate)
    if librnRegnIDforUpdate == None or librnRegnIDforUpdate.strip() == "" or librnRegnIDforUpdate == "EXIT$":
        if DEBUG_MODE:
            print("[DEBUG] :: librnRegnIDforUpdate is Null/Empty or user chose EXIT$ " + librnRegnIDforUpdate)
        return

    # Fetches the entire list of Librarian Registration IDs from the DB
    response_librnRegnIDs = cOps.getLibrarianRegnIDsFromLibrariansTbl()
    if DEBUG_MODE:
        print(f"[DEBUG] :: response_librnRegnIDs :: {response_librnRegnIDs} ")

    if (response_librnRegnIDs != None and len(response_librnRegnIDs) > 0 and response_librnRegnIDs[0] == 1 and
            response_librnRegnIDs[1] is not None and len(response_librnRegnIDs[1]) > 0):
        for librnRegnID_tpl in response_librnRegnIDs[1]:
            if librnRegnIDforUpdate not in librnRegnID_tpl:
                print(f"{librnRegnIDforUpdate} not in {librnRegnID_tpl} \nHence continuing search...")
                continue
            else:
                if DEBUG_MODE:
                    print(f"[DEBUG] :: {librnRegnIDforUpdate}  found in DB Librarian Registration IDs' list.")
                    print(f"[DEBUG] :: Calling getLibrarianInfo() by sending {librnRegnIDforUpdate} ")
                response_LibrarianInfo = cOps.getLibrarianInfo(librnRegnIDforUpdate)
                if DEBUG_MODE:
                    print(
                        f"[DEBUG] :: Fetched Librarian details for Librarian Registration ID :: {librnRegnIDforUpdate}  :: "
                        f"\n{response_LibrarianInfo}")

                if (response_LibrarianInfo != None and response_LibrarianInfo[0] == 1 and
                        response_LibrarianInfo[1] != None and len(response_LibrarianInfo[1]) == 1):

                    print(f"[DEBUG] :: Checking response_LibrarianInfo[1][0] :: {response_LibrarianInfo[1][0]}")
                    if (response_LibrarianInfo[1][0] != None and len(response_LibrarianInfo[1][0]) == 7):
                        if DEBUG_MODE:
                            print("[DEBUG] :: Assigning the fetched Librarian Info to Librarian object.")

                        librnObj = Librarian(response_LibrarianInfo[1][0])
                        if (librnObj is not None):
                            updtLibrarianList = librnVw.fetchLibrarianUpdateDetails(CURRENT_USER_NAME,
                                                                                    CURRENT_USER_REGN_ID, librnObj)
                            if (updtLibrarianList != None and type(
                                    updtLibrarianList) == str and updtLibrarianList == "EXIT$"):
                                if DEBUG_MODE:
                                    print(
                                        "[DEBUG] :: Looks like user chose to EXIT$ :: updtLibrarianList :: {updtLibrarianList} ")
                                    print("[DEBUG] :: Hence exiting to Main Menu!")
                                    return
                            elif (updtLibrarianList != None and len(updtLibrarianList) > 0):
                                if DEBUG_MODE:
                                    print(
                                        "[DEBUG] :: Calling updateUserInUsersTable() by Sending librnRegnIDforUpdate :: "
                                        f"{librnRegnIDforUpdate} ")

                                response_updateLibrarian = cOps.updateLibrarianDetailsInDB(librnObj.get_l_regn_num(),
                                                                                           updtLibrarianList)
                                if DEBUG_MODE:
                                    print(f"[DEBUG] :: response_updateLibrarian :: {response_updateLibrarian}")
                                if (response_updateLibrarian != None and response_updateLibrarian == 1):
                                    librnVw.showMessagesToLibrarian(
                                        ["\n_______________________________________________________________________",
                                         f"[SUCCESS] :: Successfully updated the Librarian details "
                                         f"for Librarian Registration ID :: {librnRegnIDforUpdate}",
                                         "_______________________________________________________________________"])
                                    return True
                                else:
                                    librnVw.showMessagesToLibrarian(
                                        [f"[ERROR] :: Could not update the Librarian details "
                                         f"Please contact the admin if problem persists."])
                                    return False
                            else:
                                if DEBUG_MODE:
                                    print(f"[EMPTY] :: updtLibrarianList is null/empty :: {updtLibrarianList}")
                                librnVw.showMessagesToLibrarian(
                                    ["[MESSAGE] :: Looks like you did not want to update any field.",
                                     "Hence reverting you back to the Main menu."])
                                return
                        else:
                            if DEBUG_MODE:
                                print("[ERROR] :: Librarian object could not be initialized.")
                            librnVw.showMessagesToLibrarian([
                                "[ERROR] :: Unexpected error occurred. Please report issue to Admin."])
                            return False
                    elif (response_LibrarianInfo[1][0] != None and response_LibrarianInfo[1][0] == 0):
                        if DEBUG_MODE:
                            print("[DEBUG] :: Zero records fetched from DB")
                        librnVw.showMessagesToLibrarian([
                            f"[INVALID] :: Librarian Info for Librarian Registration ID : {librnRegnIDforUpdate} "
                            f"could not be fetched.",
                            "[MESSAGE] :: Please check if you have entered a valid Librarian Registration ID and try again.",
                            "[MESSAGE] :: Contact Admin if issue still persists."])
                        return
                    else:
                        print(f"[ERROR] :: response_LibrarianInfo[1][0] :: {response_LibrarianInfo[1][0]}")
                        handleErrorsAndExceptions(response_LibrarianInfo)
                else:
                    handleErrorsAndExceptions(response_LibrarianInfo)
                    return False
        else:
            if DEBUG_MODE:
                print(f"[DEBUG] :: {librnRegnIDforUpdate} doesn't exist in the Library.")
            librnVw.showMessagesToLibrarian([
                "[INVALID] :: This Librarian Registration ID doesn't exist in our Terminal Library System",
                "[MESSAGE] :: Please check once again and enter valid Librarian Registration ID."])
            return
    else:
        handleErrorsAndExceptions(response_librnRegnIDs)
        return False


def issueBook():
    '''This method updates the Books table issued details
    Reads the book code from the librarian who would be issuing the book
    Reads the User's Registration number to whom the book would be issued to'''

    if DEBUG_MODE:
        print("[DEBUG] :: In issueBook()")

    book_code = librnVw.fetchBookCodeFromUser()
    if (book_code == None or book_code.strip() == "" or book_code == 'EXIT$'):
        if DEBUG_MODE:
            print(f"[DEBUG] :: book_code :: {book_code} is null/empty/'EXIT$'")
            print("[DEBUG] :: Hence redirecting to Main menu")
    else:
        book_availability_status = cOps.getAvailablityStatusForABook(book_code)
        if DEBUG_MODE:
            print(f"[DEBUG] :: book_availability_status :: {book_availability_status} ")
        if book_availability_status == None or type(book_availability_status) == int:
            if DEBUG_MODE:
                print("[DEBUG] :: In type check")
            librnVw.showMessagesToLibrarian(["[ERROR] :: Unexpected Response.",
                                             "Could not check the book availabilty status.",
                                             "Cannot proceed further. Hence redirecting to Main Menu."
                                             "Please contact the admin if problem persists"])
            return
        elif book_availability_status[0] != None and book_availability_status[0][0] == 'NO':
            librnVw.showMessagesToLibrarian(["[MESSAGE] :: "
                                             "This book has already been issued and is not available currently."])
            return
        elif book_availability_status[0] != None and book_availability_status[0][0] == 'YES':
            librnVw.showMessagesToLibrarian(["[MESSAGE] :: "
                                             "This book is available to be issued. Please proceed further."])
        else:
            if DEBUG_MODE:
                print("[DEBUG] :: In else while checking book_availability_status")
            librnVw.showMessagesToLibrarian(["[ERROR] :: Unexpected Response.",
                                             "Could not check the book availabilty status.",
                                             "Cannot proceed further. Hence redirecting to Main Menu."
                                             "Please contact the admin if problem persists"])
            return

    user_regn_num = librnVw.fetchUserRegnNum(CURRENT_USER_NAME)
    if (user_regn_num != None):
        response_userHasBook = cOps.checkIfUserHasABook(user_regn_num)
        if DEBUG_MODE:
            print(f"[DEBUG] :: response_userHasBook :: {response_userHasBook}")
        if (response_userHasBook == None or type(response_userHasBook) == int):
            if DEBUG_MODE:
                print(f"[DEBUG] :: response_userHasBook is Null or Exception Occurred")
        elif (len(response_userHasBook) > 0):
            librnVw.showMessagesToLibrarian(["[MESSAGE] :: Looks like you have already been issued a book.",
                                             f"Book Code :: {response_userHasBook[0][1]}",
                                             "Only one book can be issued per user at a time.",
                                             "Hence Redirecting back to Main menu."])
            return
        else:
            if DEBUG_MODE:
                print(f"[DEBUG] :: In else response_userHasBook :: {response_userHasBook}")
    else:
        if DEBUG_MODE:
            print(f"[DEBUG] :: In else This case was supposed to be handled from the view")

    issueBookTpl = (CURRENT_USER_REGN_ID, user_regn_num, book_code)

    if DEBUG_MODE:
        print(f"[DEBUG] :: book_code :: {book_code}")
        print(f"[DEBUG] :: user_regn_num :: {user_regn_num}")
        print(f"[DEBUG] :: CURRENT_USER_REGN_ID :: {CURRENT_USER_REGN_ID}")
        print("\n[DEBUG] :: Calling updateBookIssued() by passing the following : ")
        print(f"[DEBUG] :: issueBookTpl :: {issueBookTpl}")

    response_issueBook = cOps.updateBookIssued(issueBookTpl)
    if DEBUG_MODE:
        print(f"[DEBUG] :: response_issueBook :: {response_issueBook}")

    if response_issueBook == None or len(response_issueBook) != 2:
        librnVw.showMessagesToLibrarian(["[EMPTY] :: Empty or Unexpected Response.",
                                         "Could not update the book issued details.",
                                         "Please contact the admin if problem persists"])
        return
    elif response_issueBook[0] == 1:
        librnVw.showMessagesToLibrarian(["\n_______________________________________________________________________",
                                         "[SUCCESS] :: Successfully updated the book issued details "
                                         f"for the book code :: {book_code}",
                                         "_______________________________________________________________________"])
        return
    else:
        handleErrorsAndExceptions(response_issueBook)
        return


def calculateBillingAmountForUser(user_regn_num):
    '''Calculates the billing details for a user'''

    if DEBUG_MODE:
        print("[DEBUG] :: user_regn_num :: ", user_regn_num)

    totalAmount = None

    if (user_regn_num != None):
        calcAmountObj = cOps.calcAmntToBePaidAsPerToday(user_regn_num)

        # book_Code, book_Name, book_Fee, issued_Date, issued_To, issued_By
        if (calcAmountObj != None and len(calcAmountObj) > 0 and calcAmountObj[0] != None):
            try:
                if DEBUG_MODE:
                    print("[DEBUG] :: calcAmountObj :: ", calcAmountObj)
                book_Code = calcAmountObj[0][0]
                book_Name = calcAmountObj[0][1]
                book_Fee = float(calcAmountObj[0][2])
                issued_Date = calcAmountObj[0][3]
                issued_To = calcAmountObj[0][4]
                issued_By = calcAmountObj[0][5]
                today = date.today()
                date_object = datetime.strptime(issued_Date, '%Y-%m-%d').date()
                if DEBUG_MODE:
                    print("[DEBUG] :: ", book_Code, book_Name, book_Fee, issued_Date, issued_To, issued_By)
                    print("[DEBUG] :: date_object :: ", date_object)
                    print("[DEBUG] :: date_object type :: ", type(date_object))
                    print("[DEBUG] :: ", today)
                    print("[DEBUG] :: Date difference :: ", today.date() - date_object)

                daysRented = (today.date() - date_object).days.__int__()

                totalAmount = 0

                if (daysRented <= 20):
                    totalAmount = book_Fee
                    billingTpl = (user_regn_num, CURRENT_USER_NAME, book_Code, book_Name, issued_Date,
                                  today.date(), daysRented, 0, book_Fee, 0, totalAmount, issued_By)
                    usrVw.showUserAmountToBePaid(billingTpl)
                    return billingTpl
                else:
                    i = fineAmount = 0
                    fineDays = daysRented - 20
                    if DEBUG_MODE:
                        print("[DEBUG] :: fineDays :: ", fineDays)

                    fineIteration = fineDays // 5
                    if DEBUG_MODE:
                        print("[DEBUG] :: fineIteration :: ", fineIteration)

                    if fineIteration == 0:
                        totalAmount = book_Fee + 20
                        if DEBUG_MODE:
                            print("[DEBUG] :: totalAmount :: ", (totalAmount))
                        billingTpl = (user_regn_num, CURRENT_USER_NAME, book_Code, book_Name,
                                      issued_Date, today.date(), daysRented, fineDays, book_Fee, 20, totalAmount,
                                      issued_By)
                        usrVw.showUserAmountToBePaid(billingTpl)
                        return billingTpl

                    while (i < fineIteration):
                        fineAmount += 20 + (i * 5)
                        if DEBUG_MODE:
                            print("[DEBUG] :: Inside while :: fineAmount :: ", fineAmount)
                        i += 1

                    if DEBUG_MODE:
                        print("[DEBUG] :: total fineAmount :: ", fineAmount)
                        print("[DEBUG] :: totalAmount :: ", (book_Fee + fineAmount))

                    totalAmount = book_Fee + fineAmount
                    billingTpl = (user_regn_num, CURRENT_USER_NAME, book_Code, book_Name, issued_Date, today.date(),
                                  daysRented, fineDays, book_Fee, fineAmount, totalAmount, issued_By)
                    usrVw.showUserAmountToBePaid(billingTpl)
                    return billingTpl
            except ValueError as ve:
                if DEBUG_MODE:
                    print("[EXCEPT] :: Value Error occured in viewAmountToBePaid() in LibraryController")
                    print("[EXCEPT] :: Value Error :: ", ve)
                print("[EXCEPTION OCCURED] :: Sorry! Could not fetch amount details")
        elif (calcAmountObj != None and len(calcAmountObj) == 0):
            librnVw.showMessagesToLibrarian(["[INVALID] :: Seems like this User "
                                             "does not have any book to return back to the Library.",
                                             "[MESSAGE] :: Please check the User Registration Number and try again."])
        else:
            librnVw.showMessagesToLibrarian(["[ERROR] :: Unexpected Error occurred",
                                             "[MESSAGE] :: Please contact the Admin if the problem persists"])


def updateBookReturned():
    '''This method updates the Books table book returned details details
    Reads the book code from the librarian who would be issuing the book
    Reads the User's Registration number to whom the book would be issued to'''

    if DEBUG_MODE:
        print("[DEBUG] :: In updateBookReturned()")

    book_code = None

    user_regn_num = librnVw.fetchUserRegnNum(CURRENT_USER_NAME)
    if (user_regn_num != None):
        # billingReturnTpl >> (user_regn_num, CURRENT_USER_NAME, book_Code, book_Name, issued_Date, today.date(), daysRented, fineDays, book_Fee, fineAmount, totalAmount)
        billingReturnTpl = calculateBillingAmountForUser(user_regn_num)
        if DEBUG_MODE:
            print(f"[DEBUG] :: billingReturnTpl :: {billingReturnTpl} ")
        if (billingReturnTpl != None and len(billingReturnTpl) == 12):
            librnVw.showMessagesToLibrarian(["[MESSAGE] :: Please verify if the same book "
                                             f"with the book code {billingReturnTpl[2]} is being returned "
                                             f"by the user with registration ID {user_regn_num}"])
            book_code_verified = input("[INPUT] :: Should we proceed to updating the return of book? [Y] Yes [N] No ")
            if book_code_verified != None and book_code_verified == 'N':
                if DEBUG_MODE:
                    print(f"[DEBUG] :: User input book_code_verified :: {book_code_verified} ")
                    print(f"[DEBUG] :: Hence returning.. ")
                librnVw.showMessagesToLibrarian(["[MESSAGE] :: Please enter the valid Book Code and try again.."])
            elif book_code_verified == None or book_code_verified != 'Y':
                if DEBUG_MODE:
                    print(f"[DEBUG] :: User input book_code_verified :: {book_code_verified} ")
                    print(f"[DEBUG] :: Hence returning.. ")
                librnVw.showMessagesToLibrarian(["[MESSAGE] :: Please enter the valid input and try again.."])
            else:
                book_code = billingReturnTpl[2]
                issued_By = billingReturnTpl[11]
                issued_To = billingReturnTpl[0]
                issued_Date = billingReturnTpl[4]
                total_amount = billingReturnTpl[10]

                # (book_Code, issued_By, issued_To, issued_Date, return_Date, received _By, amount_Paid)
                bookReturnDetailsTpl = (
                book_code, issued_By, issued_To, issued_Date, CURRENT_USER_REGN_ID, total_amount)
                if DEBUG_MODE:
                    print("\n[DEBUG] :: Calling updateBookIssued() by passing the following : ")
                    print(f"[DEBUG] :: bookReturnDetailsTpl :: {bookReturnDetailsTpl}")

                    response_returnBook = cOps.updateBookReturned(bookReturnDetailsTpl)
                    if DEBUG_MODE:
                        print(f"[DEBUG] :: response_returnBook :: {response_returnBook}")

                    if response_returnBook == None or len(response_returnBook) != 2:
                        librnVw.showMessagesToLibrarian(["[EMPTY] :: Empty or Unexpected Response.",
                                                         "Could not update the book returned details.",
                                                         "Please contact the admin if problem persists"])
                        return
                    elif response_returnBook[0] == 1:
                        librnVw.showMessagesToLibrarian(
                            ["\n_______________________________________________________________________",
                             "[SUCCESS] :: Successfully updated the book returned details "
                             f"for the book code :: {book_code}",
                             "_______________________________________________________________________"])
                        return
                    else:
                        handleErrorsAndExceptions(response_returnBook)
                        return
        else:
            librnVw.showMessagesToLibrarian(["[EMPTY] :: Empty or Unexpected Response.",
                                             "Could not update the book returned details.",
                                             "Please contact the admin if problem persists"])
    else:
        librnVw.showMessagesToLibrarian(["[EMPTY] :: Empty or Unexpected Response.",
                                         "Could not update the book returned details.",
                                         "Please contact the admin if problem persists"])


def librarianSelectedOption(i):
    '''Reads the option selected by the Librarian and
    invokes respective functions'''

    # switcher={
    #     'A': viewAvailableBooks(),
    #     'B': viewBookDetails(),
    #     'C': addBook(),
    #     'D': updateBook(),
    #     'E': deleteBook(),
    #     'F': addUser(),
    #     'G': updateUser(),
    #     'H': deleteUser(),
    #     'I': addLibrarian(),
    #     'J': updateLibrarian(),
    #     'K': deleteLibrarian(),
    #     'L': logout(CURRENT_USER_NAME)
    # }
    # if DEBUG_MODE:
    #     print("Exiting Librarian Switcher")
    # return switcher.get(i,"You entered an Invalid Option!")

    if i == 'A':
        viewAvailableBooks()
        # return True
    elif i == 'B':
        viewBookDetails()
    elif i == 'C':
        addBook()
    elif i == 'D':
        updateBook()
    elif i == 'E':
        deleteBook()
    elif i == 'F':
        addUser()
    elif i == 'G':
        updateUser()
    elif i == 'H':
        deleteUser()
    elif i == 'I':
        addLibrarian()
    elif i == 'J':
        updateLibrarian()
    elif i == 'K':
        deleteLibrarian()
    elif i == 'L':
        issueBook()
    elif i == 'M':
        updateBookReturned()
    elif i == 'LOGOUT':
        lgnVw.logout(CURRENT_USER_NAME)
        return "LOGOUT$"
    else:
        print("[INVALID] :: Oooops! You entered an Invalid Option!")
        print("[MESSAGE] :: Try again...")


def viewAmountToBePaid():
    ''' This function calculates the amount to be paid by the User
    including the Fine amount applicable (if any)
    This function in turn sends variable values to
    UserPageView's showUserAmountToBePaid() where it formats
    and displays (Kind of a) Billing details'''
    user_regn_num = None
    totalAmount = None

    if (CURRENT_USER != None):
        userObj: User = CURRENT_USER.get('USER')
        if userObj != None:
            user_regn_num = userObj.get_u_regn_num()

    if user_regn_num != None:
        calcAmountObj = cOps.calcAmntToBePaidAsPerToday(user_regn_num)

        # book_Code, book_Name, book_Fee, issued_Date, issued_To
        if (calcAmountObj != None and len(calcAmountObj) > 0 and calcAmountObj[0] != None):
            try:
                if DEBUG_MODE:
                    print("[DEBUG] :: calcAmountObj :: ", calcAmountObj)
                book_Code = calcAmountObj[0][0]
                book_Name = calcAmountObj[0][1]
                book_Fee = float(calcAmountObj[0][2])
                issued_Date = calcAmountObj[0][3]
                issued_To = calcAmountObj[0][4]
                today = datetime.today()
                date_object = datetime.strptime(issued_Date, '%Y-%m-%d').date()
                if DEBUG_MODE:
                    print("[DEBUG] :: ", book_Code, book_Name, book_Fee, issued_Date, issued_To)
                    print("[DEBUG] :: date_object :: ", date_object)
                    print("[DEBUG] :: date_object type :: ", type(date_object))
                    print("[DEBUG] :: ", today)
                    print("[DEBUG] :: Date difference :: ", today.date() - date_object)

                daysRented = (today.date() - date_object).days.__int__()

                totalAmount = 0

                if (daysRented <= 20):
                    totalAmount = book_Fee
                    billingTpl = (user_regn_num, CURRENT_USER_NAME, book_Code, book_Name, issued_Date,
                                  today.date(), daysRented, 0, book_Fee, 0, totalAmount)
                    usrVw.showUserAmountToBePaid(billingTpl)
                    return billingTpl
                else:
                    i = fineAmount = 0
                    fineDays = daysRented - 20
                    if DEBUG_MODE:
                        print("[DEBUG] :: fineDays :: ", fineDays)

                    fineIteration = fineDays // 5
                    if DEBUG_MODE:
                        print("[DEBUG] :: fineIteration :: ", fineIteration)

                    if fineIteration == 0:
                        totalAmount = book_Fee + 20
                        if DEBUG_MODE:
                            print("[DEBUG] :: totalAmount :: ", (totalAmount))
                        billingTpl = (user_regn_num, CURRENT_USER_NAME, book_Code, book_Name,
                                      issued_Date, today.date(), daysRented, fineDays, book_Fee, 20, totalAmount)
                        usrVw.showUserAmountToBePaid(billingTpl)
                        return billingTpl

                    while (i < fineIteration):
                        fineAmount += 20 + (i * 5)
                        if DEBUG_MODE:
                            print("[DEBUG] :: Inside while :: fineAmount :: ", fineAmount)
                        i += 1

                    if DEBUG_MODE:
                        print("[DEBUG] :: total fineAmount :: ", fineAmount)
                        print("[DEBUG] :: totalAmount :: ", (book_Fee + fineAmount))

                    totalAmount = book_Fee + fineAmount
                    billingTpl = (user_regn_num, CURRENT_USER_NAME, book_Code, book_Name, issued_Date, today.date(),
                                  daysRented, fineDays, book_Fee, fineAmount, totalAmount)
                    usrVw.showUserAmountToBePaid(billingTpl)
                    return billingTpl

            except ValueError as ve:
                if DEBUG_MODE:
                    print("[EXCEPT] :: Value Error occured in viewAmountToBePaid() in LibraryController")
                    print("[EXCEPT] :: Value Error :: ", ve)
                print("[EXCEPTION OCCURED] :: Sorry! Could not fetch amount details")
        elif (calcAmountObj != None and len(calcAmountObj) == 0):
            usrVw.showMessagesToUser(["\n------------------------------------------------------------------------",
                                      "[MESSAGE] :: Seems like you have not hired any books from the Library yet.",
                                      "Hence there is no amount applicable for you to be paid.",
                                      "We do have a good set of books in our Library.",
                                      "You may hire one now...",
                                      "------------------------------------------------------------------------"])
        else:
            usrVw.showMessagesToUser(["[ERROR] :: Unexpected error occurred! Please contact the Admin"])


def viewUserDetails():
    '''This function sends the user object to the User view page
    which in turn displays the User details to the user in a formatted pattern'''

    if DEBUG_MODE:
        print("[DEBUG] :: In viewUserDetails()")

    userObj = None
    if (CURRENT_USER != None):
        userObj: User = CURRENT_USER.get('USER')
    usrVw.showUserInformation(userObj)

    if DEBUG_MODE:
        print("[DEBUG] :: Exiting viewUserDetails()")


def updateUserDetails():
    '''This function invokes fetchUserUpdateDetails() to fetch
    user update account information details.
    On successfully fetching info, it invokes UpdateUserDetailsInDB()
    to update the table in Database'''

    if DEBUG_MODE:
        print("[DEBUG] :: In updateUserDetails()")

    userObj = None
    if (CURRENT_USER != None):
        userObj: User = CURRENT_USER.get('USER')
    usrUpdtList = usrVw.fetchUserUpdateDetails(userObj)

    if (type(usrUpdtList) == str and usrUpdtList == "EXIT$"):
        return False

    if (usrUpdtList != None and len(usrUpdtList) >= 1):
        response_updtUser = cOps.UpdateUserDetailsInDB(userObj.get_u_regn_num(), usrUpdtList)
        if (response_updtUser != None and response_updtUser == 1):
            usrVw.showMessagesToUser(["_______________________________________________________________________",
                                      "[SUCCESS] :: Successfully updated User details",
                                      "[MESSAGE] :: You may see the updated changes once you re-login!",
                                      "_______________________________________________________________________"])

    if DEBUG_MODE:
        print("[DEBUG] :: Exiting updateUserDetails()")
    return


def userSelectedOption(i):
    # switcher={
    #     'A': viewAvailableBooks(),
    #     'B': viewBookDetails(),
    #     'C': viewAmountToBePaid(),
    #     'D': userUpdateUserDetails(),
    #     'E': logout(CURRENT_USER_NAME)
    # }
    # if DEBUG_MODE:
    #     print("Exiting User Switcher")
    # return switcher.get(i,"You entered an Invalid Option!")

    if i == 'A':
        viewAvailableBooks()
    elif i == 'B':
        viewBookDetails()
    elif i == 'C':
        viewAmountToBePaid()
    elif i == 'D':
        viewUserDetails()
    elif i == 'E':
        updateUserDetails()
    elif i == 'L':
        lgnVw.logout(CURRENT_USER_NAME)
        return "LOGOUT$"
    else:
        print("[INVALID] :: Oooops! You entered an Invalid Option!")
        print("[MESSAGE] :: Try again...")

    if DEBUG_MODE:
        print("[DEBUG] :: Exiting userSelectedOption()")


def enterLoginCredentials():
    '''This function invokes the required functions to read login ID & password from user.
    It validates the end user and redirects the user to the Main Menu options'''

    if DEBUG_MODE:
        print("[DEBUG] :: In enterLoginCredentials()")

    global TERMINAL_LIBRARY_APP_RUNNING

    # Reading LoginID/RegistrationID from end user
    loginID = lgnVw.getLoginID()

    # Checking if user wants to exit app
    if (loginID != None and loginID != "" and loginID == "EXIT$"):
        exit_response = input(
            "[INPUT] :: Are you sure you want to EXIT from Terminal Library App? [Y] Yes | [N] No :: ")
        if (exit_response != None and exit_response != "" and exit_response == 'Y'):
            print("\n\n[MESSAGE] :: Thank you for using Terminal Library App!!")
            print("[MESSAGE] :: CLOSING Terminal Library App!!")
            TERMINAL_LIBRARY_APP_RUNNING = False
            return
        elif (exit_response != None and exit_response != "" and exit_response == 'N'):
            print("\n\n[MESSAGE] :: Please Login again!!")
            TERMINAL_LIBRARY_APP_RUNNING = True
            return
        else:
            print("\n\n[INVALID] :: You entered an invalid option!!")

    # Reading password from end user
    password = lgnVw.getPassword()

    if (loginID == None or loginID == "" or password == None or password == ""):
        print("[EMPTY] :: Null/Empty credentials given! Please enter valid login credentials. ")
    elif (password == "F$P$"):
        print("[MESSAGE] :: Forgotten Password? Please contact Librarian/Admin. ")
    elif (loginID == "admin$" and password == "admin$"):
        print("\n[MESSAGE] :: Welcome, Admin! What would you like to do?\n")
        interactWithAdmin()
    elif loginID.startswith('U'):
        response_isValidUser = lgnValidator.isValidUser('U', loginID, password)
        if (response_isValidUser == None or len(response_isValidUser) != 2):
            print("[ERR] :: Please report this issue to Librarian/Admin")
            if DEBUG_MODE:
                print("[EMPTY] :: Invalid response from LoginValidator's isValidUser() : \n", response_isValidUser)
            return False
        elif (response_isValidUser[0] == 1):
            if DEBUG_MODE:
                print("[DEBUG] :: Response Len :: ", len(response_isValidUser[1]))
                print("[DEBUG] :: Response :: ", response_isValidUser[1])
            if (len(response_isValidUser[1][0]) != 7):
                print("[DEBUG] :: Object Unexpected!! Retrieved User record list doesn't have expected 7 elements")
                print("[DEBUG] :: Length of response_isValidUser[1][0] ::", len(response_isValidUser[1][0]))
                return False
            else:
                validUser = User(response_isValidUser[1][0])
                print(f"\nDear {validUser.get_u_name()}, \n\tWelcome to Terminal Library App!!")
                print("How may I help you today? ")
                interactWithUser(validUser)
        elif (response_isValidUser[0] == 0):
            print("\n[INVALID] :: Uh-oh! Looks like you entered a wrong password!!")
            print("[MESSAGE] :: Please login again with the valid login credentials.")
            return False
        elif (response_isValidUser[0] == 2):
            print("[MESSAGE] :: Could not fetch record from Users table")
            return False
        elif (response_isValidUser[0] == 99):
            print("[INVALID] :: Invalid Login/Registration ID | ID doesn't start with 'U' or 'L' ")
            return False
        elif (response_isValidUser[0] == 100):
            print("[EXCEPT] :: Exception Occured!!")
            return False
    elif loginID.startswith('L'):
        response_isValidUser = lgnValidator.isValidUser('L', loginID, password)
        if (response_isValidUser == None or len(response_isValidUser) != 2):
            print("[ERR] :: Please report this issue to Librarian/Admin")
            if DEBUG_MODE:
                print("[EMPTY] :: Invalid response from LoginValidator's isValidUser() : \n", response_isValidUser)
            return False
        elif (response_isValidUser[0] == 1):
            if DEBUG_MODE:
                print("[DEBUG] :: Response Len :: ", len(response_isValidUser[1]))
                print("[DEBUG] :: Response :: ", response_isValidUser[1])
            if (len(response_isValidUser[1][0]) != 7):
                if DEBUG_MODE:
                    print("[DEBUG] :: Object Unexpected!! Retrieved User record list doesn't have expected 7 elements")
                    print("[DEBUG] :: Length of response_isValidUser[1] ::", len(response_isValidUser[1][0]))
                return False
            else:
                validLibrarian = Librarian(response_isValidUser[1][0])
                print(f"\nDear {validLibrarian.get_l_name()}, \n\tWelcome to Terminal Library App!!")
                print("How may I help you today? ")
                interactWithLibrarian(validLibrarian)
        elif (response_isValidUser[0] == 0):
            print("\n[INVALID] :: Uh-oh! You entered a wrong password!!")
            print("[MESSAGE] :: Please login again with the valid login credentials.")
            return False
        elif (response_isValidUser[0] == 2):
            print("[MESSAGE] :: Could not fetch record from Users table")
            return False
        elif (response_isValidUser[0] == 99):
            print("[INVALID] :: Invalid Login/Registration ID | ID doesn't start with 'U' or 'L' ")
            return False
        elif (response_isValidUser[0] == 100):
            print("[EXCEPT] :: Exception Occured!!")
            return False
    else:
        print("\n[MESSAGE] :: Please enter valid login credentials.")

    while TERMINAL_LIBRARY_APP_RUNNING:
        enterLoginCredentials()


def triggerIfAnyNotificationToUser(user_regn_num: str):
    '''This function gets executed whenever a User logs in and
    to Notify User if any book had been hired and still with user for more than two weeks.'''

    if DEBUG_MODE:
        print("[DEBUG] :: In triggerIfAnyNotificationToUser()")

    if (user_regn_num == None):
        usrVw.showMessagesToUser(["[ERROR] :: User cannot be identified. "
                                  "Unexpected error has occurred. Please contact Admin."])
        if DEBUG_MODE:
            print("[EMPTY] :: current_user_regn_ID is null. Unexpected!! Hence returning...")
        return

    calcAmountObj = cOps.calcAmntToBePaidAsPerToday(user_regn_num)

    # book_Code, book_Name, book_Fee, issued_Date, issued_To
    if (calcAmountObj != None and len(calcAmountObj) == 1 and type(calcAmountObj[0]) == tuple and calcAmountObj[
        0] != None):
        try:
            if DEBUG_MODE:
                print("[DEBUG] :: calcAmountObj :: ", calcAmountObj)
            book_Code = calcAmountObj[0][0]
            book_Name = calcAmountObj[0][1]
            book_Fee = float(calcAmountObj[0][2])
            issued_Date = calcAmountObj[0][3]
            issued_To = calcAmountObj[0][4]
            today = datetime.today()
            date_object = datetime.strptime(issued_Date, '%Y-%m-%d').date()
            if DEBUG_MODE:
                print("[DEBUG] :: ", book_Code, book_Name, book_Fee, issued_Date, issued_To)
                print("[DEBUG] :: date_object :: ", date_object)
                print("[DEBUG] :: date_object type :: ", type(date_object))
                print("[DEBUG] :: ", today)
                print("[DEBUG] :: Date difference :: ", today.date() - date_object)

            daysRented = (today.date() - date_object).days.__int__()

            totalAmount = 0

            if (daysRented <= 20):
                totalAmount = book_Fee
                billingTpl = (user_regn_num, CURRENT_USER_NAME, book_Code, book_Name, issued_Date,
                              today.date(), daysRented, 0, book_Fee, 0, totalAmount)
                usrVw.notifyUser(billingTpl)
                return billingTpl
            else:
                i = fineAmount = 0
                fineDays = daysRented - 20
                if DEBUG_MODE:
                    print("[DEBUG] :: fineDays :: ", fineDays)

                fineIteration = fineDays // 5
                if DEBUG_MODE:
                    print("[DEBUG] :: fineIteration :: ", fineIteration)

                if fineIteration == 0:
                    totalAmount = book_Fee + 20
                    if DEBUG_MODE:
                        print("[DEBUG] :: totalAmount :: ", (totalAmount))
                    billingTpl = (user_regn_num, CURRENT_USER_NAME, book_Code, book_Name,
                                  issued_Date, today.date(), daysRented, fineDays, book_Fee, 20, totalAmount)
                    usrVw.notifyUser(billingTpl)
                    return billingTpl

                while (i < fineIteration):
                    fineAmount += 20 + (i * 5)
                    if DEBUG_MODE:
                        print("[DEBUG] :: Inside while :: fineAmount :: ", fineAmount)
                    i += 1

                if DEBUG_MODE:
                    print("[DEBUG] :: total fineAmount :: ", fineAmount)
                    print("[DEBUG] :: totalAmount :: ", (book_Fee + fineAmount))

                totalAmount = book_Fee + fineAmount
                billingTpl = (user_regn_num, CURRENT_USER_NAME, book_Code, book_Name, issued_Date, today.date(),
                              daysRented, fineDays, book_Fee, fineAmount, totalAmount)
                usrVw.notifyUser(billingTpl)
                return billingTpl

        except ValueError as ve:
            if DEBUG_MODE:
                print("[EXCEPT] :: Value Error occured in viewAmountToBePaid() in LibraryController")
                print("[EXCEPT] :: Value Error :: ", ve)
            print(
                "[EXCEPTION OCCURED] :: Sorry! Could not fetch your billing amount details. Please contact the Admin.")
    elif (calcAmountObj != None and len(calcAmountObj) == 0):
        usrVw.showMessagesToUser(["\n------------------------------------------------------------------------",
                                  "[MESSAGE] :: Seems like you have not hired any books from the Library yet.",
                                  "We do have a good set of books in our Library.",
                                  "You may hire one now...",
                                  "------------------------------------------------------------------------"])
    else:
        usrVw.showMessagesToUser(["[ERROR] :: Unexpected error occurred! Please contact the Admin"])


def triggerIfAnyNotificationsToLibrarian():
    """This function gets executed whenever a Librarian logs in and
        to Notify Librarian about all the Books that had been hired and still with User/s for more than two weeks."""
    pass


while TERMINAL_LIBRARY_APP_RUNNING:
    print("[WELCOME] :: WELCOME! To Terminal Library App!!")
    enterLoginCredentials()

if __name__ == '__main__':
    if DEBUG_MODE:
        print('Terminal Library App - started from commandline')
    print("[WELCOME] :: WELCOME! To Terminal Library App!!")
    enterLoginCredentials()
else:
    if DEBUG_MODE:
        print('Terminal Library App - Imported as a module')
    print("[WELCOME] :: WELCOME! To Terminal Library App!!")
    enterLoginCredentials()

if DEBUG_MODE:
    print("\n\n[DEBUG] :: Reached the end of LibraryController file execution!")
    print("[DEBUG] :: Exiting Terminal Library App!")
