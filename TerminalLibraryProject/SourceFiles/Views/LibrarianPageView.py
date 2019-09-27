# LibrarianPageView.py

from SourceFiles.Beans import Book
from SourceFiles.Beans.Book import Book

# Global variable for Debug statements
from SourceFiles.Beans.Librarian import Librarian
from SourceFiles.Beans.User import User
from SourceFiles.Validations import CommonValidations as cVal
from SourceFiles.Commons.CommonIncludes import DEBUG_MODE


# DEBUG_MODE = False

# Some Keywords that cannot be used as like setting passwords, etc
KEYWORDSLIST = ['F$P$', 'admin$', 'EXIT$, LOGOUT$']

# Dynamic assignment to prepare the query
# Database User table column names
U_NAME = 'user_Name'
U_PWD = 'user_Password'
U_ADDRESS = 'user_Address'
U_EMAIL = 'user_EMail'
U_PHONE = 'user_Phone'

L_NAME = 'librn_Name'
L_PWD = 'librn_Password'
L_ADDRESS = 'librn_Address'
L_EMAIL = 'librn_EMail'
L_PHONE = 'librn_Phone'

# Database Book table column names
BK_NAME = "book_Name"
BK_AUTHOR = "book_Author"
BK_PUBLICATION = "book_Publication"
BK_CATEGORY = "book_Category"
BK_FEE = "book_Fee"

BK_ISSUED_BY = "issued_By"
BK_ISSUED_TO = "issued_To"
BK_ISSUED_DATE = "issued_Date"
BK_AVL_STATUS = "availability_status"

BK_RECEIVED_BY = "received_By"
BK_RETURNED_DATE = "returned_Date"

# Database Librarian table column names
LIBRN_NAME = "librn_Name"
LIBRN_PASSWORD = "librn_Password"
LIBRN_ADDRESS = "librn_Address"
LIBRN_EMAIL = "librn_EMail"
LIBRN_PHONE = "librn_Phone"


def showLibrarianOptions(username):
    '''This function Reads option from Librarian
    @:param username - just for a customized greeting '''

    print(f"\nDear {username}! Choose an option from the below list : ")
    print("--------------------------------------")

    print("[A] : View Available Books in the Library")
    print("[B] : View Book details")
    print("[C] : Add a Book")
    print("[D] : Update Book details")
    print("[E] : Delete a Book")
    print("[F] : Add a User")
    print("[G] : Update User details")
    print("[H] : Delete User")
    print("[I] : Add a Librarian")
    print("[J] : Update Librarian details")
    print("[K] : Delete a Librarian")
    print("[L] : Issue A Book ")
    print("[M] : Accept Book Returned")
    print("[LOGOUT] : Logout")

    librn_option = input("\n[INPUT] :: Please enter an option :: ")
    return librn_option


def showAvailableBooks(availableBooksList):
    '''This function displays the list of books & its details in a formatted way
    @:param List - list of avalable books'''

    if DEBUG_MODE:
        print("[DEBUG] :: In showAvailableBooks()")

    print("\n[MESSAGE] :: ")
    if availableBooksList != None and len(availableBooksList) >= 1:

        if (len(availableBooksList) == 1):
            print("Book Details :: ")
        else:
            print("List of books available in the Library :: ")

        print("Total number of books to display :: ", len(availableBooksList))

        for book in availableBooksList:
            # SELECT book_Code, book_Name, book_Author, book_Publication, book_Category, book_Fee FROM Books
            print("---------------------------------------------")
            print("Book Code :: ", book[0])
            print("Book Name :: ", book[1])
            print("Book Author :: ", book[2])
            print("Book Publication :: ", book[3])
            print("Book Category :: ", book[4])
            print("Book Fee :: ", book[5])
            print("---------------------------------------------")
    else:
        print("[EMPTY] :: Sorry! No books available! ")

    return True


def fetchBookCodeFromUser():
    '''This function reads a valid book code from the end user
    @:return book code (:String) OR  'EXIT$' to send exit to main menu message to controller'''
    book_Code: str = input("[INPUT] :: Please enter Book Code :: ")
    if(book_Code == None or book_Code.strip() == ""):
        print("[EMPTY] :: Could not read from you. You entered an empty value.")
        print("[MESSAGE] :: Please try again or enter 'EXIT$' if you would like to exit back to Main Menu")
        fetchBookCodeFromUser()
    elif book_Code.strip() == "EXIT$":
        return "EXIT$"
    elif not book_Code.strip().startswith('B'):
        print("[INVALID] :: Looks like this isn't a valid book code. As the code isn't starting with 'B'")
        print("[INVALID] :: Please enter a valid one. Try again. Or enter 'EXIT$' to exit back to Main Menu")
        fetchBookCodeFromUser()
    else:
        return book_Code


def isfloat(value):
    '''This function checks if the value is a float/decimal number
    @:param value to be checked
    :return 'True' if it is a float value, 'False' otherwise '''

    try:
        float(value)
        return True
    except ValueError:
        return False


def fetchNewBookDetails(username):
    '''This function accepts the new book details from the librarian
    to add a new book to the Library App Database Table
        @:param username - just for a customized greeting '''

    newBookObj = None

    print(f"\nDear {username}! \n\tYou have chosen to add a new book to the Library")
    print("Please enter the new book details")

    book_name = input("[INPUT] :: Please enter the new book name :: ")
    if (book_name == None or book_name.strip() == ""):
        print("[EMPTY] :: Book Name that you entered is null / empty.")
        print("[MESSAGE] :: Please enter the new book details again")
        fetchNewBookDetails(username)

    book_author = input("[INPUT] :: Please enter the new book's author :: ")
    if (book_author == None or book_author.strip() == ""):
        print("[EMPTY] :: Book Author that you entered is null / empty.")
        print("[MESSAGE] :: Please enter the new book details again")
        fetchNewBookDetails(username)

    book_publication = input("[INPUT] :: Please enter the new book's publication name :: ")
    if (book_publication == None or book_publication.strip() == ""):
        print("[EMPTY] :: Book Publication that you entered is null / empty.")
        print("[MESSAGE] :: Please enter the new book details again")
        fetchNewBookDetails(username)

    book_category = input("[INPUT] :: Please enter the new book category :: ")
    if (book_category == None or book_category.strip() == ""):
        print("[EMPTY] :: Book Category that you entered is null / empty.")
        print("[MESSAGE] :: Please enter the new book details again")
        fetchNewBookDetails(username)

    book_fee = input("[INPUT] :: Please enter the new book's fee amount :: ")
    if (book_fee == None or book_fee.strip() == ""):
        print("[EMPTY] :: Book Fee Amount that you entered is null / empty.")
        print("[MESSAGE] :: Please enter the new book details again")
        fetchNewBookDetails(username)

    elif (isfloat(book_fee) == False):
        print("[INVALID] :: Book Fee Amount that you entered is not an Integer or decimal")
        print("[MESSAGE] :: Please enter the new book details again")
        fetchNewBookDetails(username)

    elif (float(book_fee) < 0.0):
        print("[INVALID] :: Book Fee Amount cannot be a negative number")
        print("[MESSAGE] :: Please enter the new book details again")
        fetchNewBookDetails(username)

    book_name = book_name.replace("'", "''")
    book_author = book_author.replace("'", "''")
    book_publication = book_publication.replace("'", "''")
    book_category = book_category.replace("'", "''")

    newBookTpl = (0, "", book_name, book_author, book_publication, book_category, book_fee, None, None, None, "YES")
    newBookObj = Book(newBookTpl)

    return newBookObj


def fetchBookCodeToDeleteBook(username):
    '''This function reads the book code from librarian for the deletion of book in the Library App'''
    print(f"[MESSAGE] :: Dear {username}, \n\tAre you sure? Do you really want to delete a book from the Library App?")
    print("[MESSAGE] :: Enter 'MENU$' if you would want to go back to the Main menu.")
    book_Code = input("[INPUT] :: Enter Book Code of the book you would want to delete :: ")
    if (book_Code == None or book_Code.strip() == ""):
        print("[EMPTY] :: book code that you entered was either null/empty.")
        print("[MESSAGE] :: Please try again...")
        fetchBookCodeToDeleteBook(username)
    elif (book_Code == "MENU$"):
        print("[MESSAGE] :: You chose to exit to Main menu. Hence redirecting...")
        return 'EXIT$'
    elif (book_Code.strip().startswith('B') == False):
        print("[INVALID] :: Invalid book code! Book Code doesn't start with 'B'")
        print("[MESSAGE] :: Please enter a valid Book Code")
        fetchBookCodeToDeleteBook(username)
    else:
        return book_Code


def fetchBookDetailsForUpdate(username, bookObj: Book):
    '''This function accepts the updates for book details from the librarian
    to update a book in the Library App Database Table
            @:param username - just for a customized greeting
            @:param Book object
            @:return List - [book code, [Table column name, updated value]'''

    if DEBUG_MODE:
        print("[DEBUG] :: in fetchBookDetailsForUpdate()")

    print(f"\nDear {username}! \n\tYou have chosen to update book details.")
    print('Please enter the book details for update')

    updtBookList = []

    if (bookObj != None):
        print("\nThe book details of the ")
        print("Book Code :: ", bookObj.get_bk_Code())
        print("---------------------------------------------")
        print("Book Name :: ", bookObj.get_bk_name())
        print("Book Author :: ", bookObj.get_bk_author())
        print("Book Publication :: ", bookObj.get_bk_publication())
        print("Book Category :: ", bookObj.get_bk_category())
        print("Book Fee :: ", bookObj.get_bk_fee())
        print("---------------------------------------------")

        bkNameFlag = True
        while (bkNameFlag):
            user_response = input("[INPUT] :: Would you like to update Book Name ? [Y] Yes | [N] No  [E$] Exit :: ")
            if (user_response == 'Y'):
                user_response = input("[INPUT] :: Please enter the book name for update :: ")
                if (user_response == None or user_response.strip() == ""):
                    print("[EMPTY] :: Book Name that you entered is null / empty.")
                    print("[MESSAGE] :: Please enter the new book details again")
                    continue
                else:
                    user_response = user_response.replace("'", "''")
                    user_response = "\'" + user_response + "\'"
                    updtBookList.append([BK_NAME, user_response])
                    bkNameFlag = False
                    break
            elif user_response == 'N':
                break
            elif user_response == 'E$':
                user_response = input(
                    "[INPUT] :: Are you sure you want to Exit back to the Main menu without updating?? \n[Y] Yes | [N] No :: ")
                if (user_response == 'Y'):
                    return "EXIT$"
            else:
                print("[INVALID] :: Invalid input. Please try again")
                continue

        bkAuthorFlag = True
        while (bkAuthorFlag):
            user_response = input("[INPUT] :: Would you like to update Book's Author info ? [Y] Yes | [N] No  [E$] Exit :: ")
            if (user_response == 'Y'):
                user_response = input("[INPUT] :: Please enter the book's author for update :: ")
                if (user_response == None or user_response.strip() == ""):
                    print("[EMPTY] :: Book Author that you entered is null / empty.")
                    print("[MESSAGE] :: Please enter the new book details again")
                    continue
                else:
                    user_response = user_response.replace("'", "''")
                    user_response = "\'" + user_response + "\'"
                    updtBookList.append([BK_AUTHOR, user_response])
                    bkAuthorFlag = False
                    break
            elif user_response == 'N':
                break
            elif user_response == 'E$':
                user_response = input(
                    "[INPUT] :: Are you sure you want to Exit back to the Main menu without updating?? \n[Y] Yes | [N] No :: ")
                if (user_response == 'Y'):
                    return "EXIT$"
            else:
                print("[INVALID] :: Invalid input. Please try again")
                continue

        bkPblcnFlag = True
        while (bkPblcnFlag):
            user_response = input(
                "[INPUT] :: Would you like to update Book's Publication info ? [Y] Yes | [N] No  [E$] Exit :: ")
            if (user_response == 'Y'):
                user_response = input("[INPUT] :: Please enter the book's publication info for update :: ")
                if (user_response == None or user_response.strip() == ""):
                    print("[EMPTY] :: Book Author that you entered is null / empty.")
                    print("[MESSAGE] :: Please enter the new book details again")
                    continue
                else:
                    user_response = user_response.replace("'", "''")
                    user_response = "\'" + user_response + "\'"
                    updtBookList.append([BK_PUBLICATION, user_response])
                    bkPblcnFlag = False
                    break
            elif user_response == 'N':
                break
            elif user_response == 'E$':
                user_response = input(
                    "[INPUT] :: Are you sure you want to Exit back to the Main menu without updating?? \n[Y] Yes | [N] No :: ")
                if (user_response == 'Y'):
                    return "EXIT$"
            else:
                print("[INVALID] :: Invalid input. Please try again")
                continue

        bkCtgryFlag = True
        while (bkCtgryFlag):
            user_response = input(
                "[INPUT] :: Would you like to update Book's Category info ? [Y] Yes | [N] No  [E$] Exit :: ")
            if (user_response == 'Y'):
                user_response = input("[INPUT] :: Please enter the book's category info for update :: ")
                if (user_response == None or user_response.strip() == ""):
                    print("[EMPTY] :: Book Category info that you entered is null / empty.")
                    print("[MESSAGE] :: Please enter the new book details again")
                    continue
                else:
                    user_response = user_response.replace("'", "''")
                    user_response = "\'" + user_response + "\'"
                    updtBookList.append([BK_CATEGORY, user_response])
                    bkCtgryFlag = False
                    break
            elif user_response == 'N':
                break
            elif user_response == 'E$':
                user_response = input(
                    "[INPUT] :: Are you sure you want to Exit back to the Main menu without updating?? \n[Y] Yes | [N] No :: ")
                if (user_response == 'Y'):
                    return "EXIT$"
            else:
                print("[INVALID] :: Invalid input. Please try again")
                continue

        bkFeeFlag = True
        while (bkFeeFlag):
            user_response = input(
                "[INPUT] :: Would you like to update Book's Fee amount ? [Y] Yes | [N] No  [E$] Exit :: ")
            if (user_response == 'Y'):
                user_response = input("[INPUT] :: Please enter the book's fee amount for update :: ")
                if (user_response == None or user_response.strip() == ""):
                    print("[EMPTY] :: Book Fee amount that you entered is null / empty.")
                    print("[MESSAGE] :: Please enter the new book details again")
                    continue
                elif (isfloat(user_response) == False):
                    print("[INVALID] :: Book Fee Amount that you entered is not an Integer or decimal")
                    print("[MESSAGE] :: Please enter the new book details again")
                    continue
                elif (float(user_response) < 0.0):
                    print("[INVALID] :: Book Fee Amount cannot be a negative number")
                    print("[MESSAGE] :: Please enter the new book details again")
                    continue
                else:
                    updtBookList.append([BK_FEE, user_response])
                    bkFeeFlag = False
                    break
            elif user_response == 'N':
                break
            elif user_response == 'E$':
                user_response = input(
                    "[INPUT] :: Are you sure you want to Exit back to the Main menu without updating?? \n[Y] Yes | [N] No :: ")
                if (user_response == 'Y'):
                    return "EXIT$"
            else:
                print("[INVALID] :: Invalid input. Please try again")
                continue
    else:
        showMessagesToLibrarian(["[ERROR] :: Book details could not be fetched before Updating"])
        return None

    if DEBUG_MODE:
        print(f"[DEBUG] :: Exiting fetchBookDetailsForUpdate(), Returning updtBookList :: {updtBookList}")
    return [bookObj.get_bk_Code(), updtBookList]


def showMessagesToLibrarian(msgsList: list):
    '''This function displays messages to the user
    @:param List - List of String messages'''

    if (msgsList is not None and len(msgsList) > 0):
        for msg in msgsList:
            print(msg)


def fetchNewUserDetails(current_user_name):
    '''This function accepts the new User details from the librarian
        to add a new User to the Library App Database Table
            @:param current_user_name - just for a customized greeting '''

    newUserTpl = None

    print(f"\nDear {current_user_name}! \n\tYou have chosen to add a new User to the Terminal Library App")
    print("Please enter the new User details")

    while True:
        user_name = input("[INPUT] :: Please enter the new User name :: ")
        if (user_name == None or user_name.strip() == ""):
            print("[EMPTY] :: User Name that you entered is null / empty.")
            print("[MESSAGE] :: Please try again, Or type 'EXIT$' to exit back to the Main menu.")
            continue
        elif("'" in user_name):
            print("[INVALID] :: Single quote character ' invalid in a Name. Please try again.")
            continue
        else:
            break

    while True:
        print("[MESSAGE] :: Password can be later changed by the user, for now you can set a temporary password.")
        user_password = input("[INPUT] :: Please enter the new user's temporary password :: ")
        if (user_password == None or user_password.strip() == ""):
            print("[EMPTY] :: Password that you entered is null / empty.")
            continue
        elif (user_password in KEYWORDSLIST):
            print("[INVALID] :: Some Keywords are restricted from being set as passwords.")
            print("Please try again.")
            continue
        elif ("'" in user_password):
            print("[INVALID] :: Single quote character ' invalid in a password. Please try again.")
            continue
        else:
            break

    while True:
        user_address = input("[INPUT] :: Please enter the new User's address :: ")
        if (user_address == None or user_address.strip() == ""):
            print("[EMPTY] :: User's Address that you entered is null / empty.")
            print("[MESSAGE] :: Please try again, Or type 'EXIT$' to exit back to the Main menu.")
            continue
        else:
            user_address = user_address.replace("'", "''")
            break

    while True:
        user_email = input("[INPUT] :: Please enter the new User's Email ID :: ")
        if (user_email == None or user_email.strip() == ""):
            print("[EMPTY] :: User Email ID that you entered is null / empty.")
            print("[MESSAGE] :: Please try again, Or type 'EXIT$' to exit to the Main menu.")
            continue
        elif (cVal.isEmailValid(user_email) == False):
            print("[INVALID] :: Not a valid E-Mail ID. Please enter a valid one Or type 'EXIT$' to exit to the Main menu.")
            continue
        else:
            break

    while True:
        user_phone = input("[INPUT] :: Please enter the new User's Phone number :: ")
        if (user_phone == None or user_phone.strip() == ""):
            print("[EMPTY] :: User's Phone number that you entered is null / empty.")
            print("[MESSAGE] :: Please try again, Or type 'EXIT$' to exit back to the Main menu.")
            continue
        elif (cVal.isPhoneValid(user_phone) == False):
            print("[INVALID] :: Not a valid Phone number. Please enter a valid one..")
            continue
        else:
            break

    newUserTpl = (0, "", user_password, user_name, user_address, user_email, user_phone)
    newUserObj:User = User(newUserTpl)

    return newUserObj


def fetchNewLibrarianDetails(current_user_name):
    '''This function accepts the new Librarian details from the librarian
        to add a new Librarian to the Library App Database Table
            @:param current_user_name - just for a customized greeting '''

    newLibrarianTpl = None

    print(f"\nDear {current_user_name}! \n\tYou have chosen to add a new Librarian to the Terminal Library App")
    print("Please enter the new Librarian details")

    while True:
        librn_name = input("[INPUT] :: Please enter the new Librarian name :: ")
        if (librn_name == None or librn_name.strip() == ""):
            print("[EMPTY] :: Librarian Name that you entered is null / empty.")
            print("[MESSAGE] :: Please try again, Or type 'EXIT$' to exit back to the Main menu.")
            continue
        elif ("'" in librn_name):
            print("[INVALID] :: Single quote character ' invalid in a Name. Please try again.")
            continue
        else:
            break

    while True:
        print("[MESSAGE] :: Password can be later changed by the new Librarian, "
              "for now you can set a temporary password.")
        librn_password = input("[INPUT] :: Please enter the new Librarian's temporary password :: ")
        if (librn_password == None or librn_password.strip() == ""):
            print("[EMPTY] :: Password that you entered is null / empty.")
            continue
        elif (librn_password in KEYWORDSLIST):
            print("[INVALID] :: Some Keywords are restricted from being set as passwords.")
            print("Please try again.")
            continue
        elif ("'" in librn_password):
            print("[INVALID] :: Single quote character ' invalid in a password. Please try again.")
            continue
        else:
            break

    while True:
        librn_address = input("[INPUT] :: Please enter the new Librarian's address :: ")
        if (librn_address == None or librn_address.strip() == ""):
            print("[EMPTY] :: Librarian's Address that you entered is null / empty.")
            print("[MESSAGE] :: Please try again, Or type 'EXIT$' to exit back to the Main menu.")
            continue
        else:
            librn_address = librn_address.replace("'", "''")
            break

    while True:
        librn_email = input("[INPUT] :: Please enter the new Librarian's Email ID :: ")
        if (librn_email == None or librn_email.strip() == ""):
            print("[EMPTY] :: Librarian's Email ID that you entered is null / empty.")
            print("[MESSAGE] :: Please try again, Or type 'EXIT$' to exit to the Main menu.")
            continue
        elif (cVal.isEmailValid(librn_email) == False):
            print(
                "[INVALID] :: Not a valid E-Mail ID. Please enter a valid one "
                "Or type 'EXIT$' to exit to the Main menu.")
            continue
        else:
            break

    while True:
        librn_phone = input("[INPUT] :: Please enter the new Librarian's Phone number :: ")
        if (librn_phone == None or librn_phone.strip() == ""):
            print("[EMPTY] :: Librarian's Phone number that you entered is null / empty.")
            print("[MESSAGE] :: Please try again, Or type 'EXIT$' to exit back to the Main menu.")
            continue
        elif (cVal.isPhoneValid(librn_phone) == False):
            print("[INVALID] :: Not a valid Phone number. Please enter a valid one..")
            continue
        else:
            break

    newLibrarianTpl = (0, "", librn_password, librn_name, librn_address, librn_email, librn_phone)
    newLibrarianObj:Librarian = Librarian(newLibrarianTpl)

    return newLibrarianObj


def fetchUserRegnNumToDeleteUser(current_user_name):
    '''Reads User's registration number from Librarian for user account deletion '''
    print(f"[MESSAGE] :: Dear {current_user_name}, \n\tAre you sure? Do you really want to delete a User from the Library App?")
    print("[MESSAGE] :: Enter 'MENU$' if you would want to go back to the Main menu.")
    user_regn_num = input("[INPUT] :: Enter Registration number of the User you would want to delete :: ")
    if (user_regn_num == None or user_regn_num.strip() == ""):
        print("[EMPTY] :: User's Registration number that you entered was either null/empty.")
        print("[MESSAGE] :: Please try again...")
        fetchUserRegnNumToDeleteUser(current_user_name)
    elif (user_regn_num == "MENU$"):
        print("[MESSAGE] :: You chose to exit to Main menu. Hence redirecting...")
        return 'EXIT$'
    elif (user_regn_num.strip().startswith('U') == False):
        print("[INVALID] :: Invalid Registration number! User's Registration number isn't starting with 'U'")
        print("[MESSAGE] :: Please enter a valid Book Code")
        fetchUserRegnNumToDeleteUser(current_user_name)
    else:
        return user_regn_num

def fetchLibrarianRegnNumToDeleteLibrarian(current_user_name):
    '''Reads User's registration number from Librarian for user account deletion '''
    print(f"[MESSAGE] :: Dear {current_user_name}, \n\tAre you sure? Do you really want to delete a Librarian from the Library App?")
    print("[MESSAGE] :: Enter 'MENU$' if you would want to go back to the Main menu.")
    librn_regn_num = input("[INPUT] :: Enter Registration number of the Librarian you would want to delete :: ")
    if (librn_regn_num == None or librn_regn_num.strip() == ""):
        print("[EMPTY] :: Librarian's Registration number that you entered was either null/empty.")
        print("[MESSAGE] :: Please try again...")
        fetchLibrarianRegnNumToDeleteLibrarian(current_user_name)
    elif (librn_regn_num == "MENU$"):
        print("[MESSAGE] :: You chose to exit to Main menu. Hence redirecting...")
        return 'EXIT$'
    elif (librn_regn_num.strip().startswith('L') == False):
        print("[INVALID] :: Invalid Registration number! Librarian's Registration number isn't starting with 'L'")
        print("[MESSAGE] :: Please enter a valid Book Code")
        fetchLibrarianRegnNumToDeleteLibrarian(current_user_name)
    else:
        return librn_regn_num


def fetchLibrarianRegnNum(current_user_name):
    '''Reads Librarian's registration number from Librarian '''
    if DEBUG_MODE:
        print("[DEBUG] :: In fetchLibrarianRegnNum()")
    print("[MESSAGE] :: Enter 'MENU$' if you would want to go back to the Main menu.")
    librn_regn_num = input("[INPUT] :: Enter Librarian's Registration number :: ")
    if (librn_regn_num == None or librn_regn_num.strip() == ""):
        print("[EMPTY] :: Librarian's Registration number that you entered was either null/empty.")
        print("[MESSAGE] :: Please try again...")
        fetchLibrarianRegnNum(current_user_name)
    elif (librn_regn_num == "MENU$"):
        print("[MESSAGE] :: You chose to exit to Main menu. Hence redirecting...")
        return 'EXIT$'
    elif (librn_regn_num.strip().startswith('L') == False):
        print("[INVALID] :: Invalid Registration number! Librarian's Registration number isn't starting with 'L'")
        print("[MESSAGE] :: Please enter a valid Book Code")
        fetchLibrarianRegnNum(current_user_name)
    else:
        return librn_regn_num


def fetchUserRegnNum(current_user_name):
    '''Reads User's registration number from Librarian '''
    if DEBUG_MODE:
        print("[DEBUG] :: In fetchUserRegnNum()")
    print("[MESSAGE] :: Enter 'MENU$' if you would want to go back to the Main menu.")
    user_regn_num = input("[INPUT] :: Enter User's Registration number :: ")
    if (user_regn_num == None or user_regn_num.strip() == ""):
        print("[EMPTY] :: User's Registration number that you entered was either null/empty.")
        print("[MESSAGE] :: Please try again...")
        fetchUserRegnNum(current_user_name)
    elif (user_regn_num == "MENU$"):
        print("[MESSAGE] :: You chose to exit to Main menu. Hence redirecting...")
        return 'EXIT$'
    elif (user_regn_num.strip().startswith('U') == False):
        print("[INVALID] :: Invalid Registration number! User's Registration number isn't starting with 'U'")
        print("[MESSAGE] :: Please enter a valid Book Code")
        fetchUserRegnNum(current_user_name)
    else:
        return user_regn_num


def fetchUserUpdateDetails(current_user_name, userObj:User):
    '''This function fetches the User account update related information details from  User
        @param current User object'''

    if DEBUG_MODE:
        print("[DEBUG] :: In fetchUserUpdateDetails().")

    print(f"Hello, {current_user_name}! \n\tYou have chosen to update a User's Account information ")
    print("--------------------------------------------------------------------")

    userUpdateInfoList = []

    if (userObj != None):
        print("\nThe User's details are as follows :: ")
        print("User Registration ID :: ", userObj.get_u_regn_num())
        print("---------------------------------------------")
        print("User Name :: ", userObj.get_u_name())
        print("User Address :: ", userObj.get_u_address())
        print("User Email :: ", userObj.get_u_email())
        print("User Phone # :: ", userObj.get_u_phone())
        print("---------------------------------------------")

        nameFlag = True
        while (nameFlag):
            user_response = input("[INPUT] :: Would you like to update User's Display Name ? [Y] Yes | [N] No  [E$] Exit :: ")
            if(user_response == 'Y'):
                user_response = input("[INPUT] :: Please enter the new Display Name :: ")
                if(user_response == None or user_response.strip() == ""):
                    print("[EMPTY] :: Null/Empty input. Please try again")
                    continue
                elif ("'" in user_response):
                    print("[INVALID] :: Invalid input. Single quote ' character not valid in a Name string. Try again.")
                    continue
                else:
                    user_response = "\'" + user_response + "\'"
                    userUpdateInfoList.append([U_NAME, user_response])
                    nameFlag = False
                    break
            elif user_response == 'N':
                break
            elif user_response == 'E$':
                user_response = input("[INPUT] :: Are you sure you want to Exit back to the Main menu without updating?? \n[Y] Yes | [N] No :: ")
                if(user_response == 'Y'):
                    return "EXIT$"
            else:
                print("[INVALID] :: Invalid input. Please try again")
                continue

        addressFlag = True
        while (addressFlag):
            user_response = input("[INPUT] :: Would you like to update User's Address ? [Y] Yes | [N] No  [E$] Exit :: ")
            if (user_response == 'Y'):
                user_response = input("[INPUT] :: Please enter the new Address information :: ")
                if (user_response == None or user_response.strip() == ""):
                    print("[EMPTY] :: Null/Empty input. Please try again")
                    continue
                else:
                    user_response = user_response.replace("'", "''")
                    user_response = "\'" + user_response + "\'"
                    userUpdateInfoList.append([U_ADDRESS, user_response])
                    addressFlag = False
                    break
            elif user_response == 'N':
                break
            elif user_response == 'E$':
                user_response = input("[INPUT] :: Are you sure you want to Exit back to the Main menu without updating?? \n[Y] Yes | [N] No :: ")
                if (user_response == 'Y'):
                    return "EXIT$"
            else:
                print("[INVALID] :: Invalid input. Please try again")
                continue

        emailFlag = True
        while (emailFlag):
            user_response = input("[INPUT] :: Would you like to update User's E-Mail ID ? [Y] Yes | [N] No  [E$] Exit :: ")
            if (user_response == 'Y'):
                user_response = input("[INPUT] :: Please enter the new E-Mail ID :: ")
                if (user_response == None or user_response.strip() == ""):
                    print("[EMPTY] :: Null/Empty input. Please try again")
                    continue
                elif(cVal.isEmailValid(user_response) == False):
                    print("[INVALID] :: Not a valid E-Mail ID. Please enter a valid one..")
                    continue
                else:
                    user_response = "\'" + user_response + "\'"
                    userUpdateInfoList.append([U_EMAIL, user_response])
                    if DEBUG_MODE:
                        print("[DEBUG] :: Appending email update to the userUpdateInfoList")
                    emailFlag = False
                    break
            elif user_response == 'N':
                break
            elif user_response == 'E$':
                user_response = input("[INPUT] :: Are you sure you want to Exit back to the Main menu without updating?? \n[Y] Yes | [N] No :: ")
                if (user_response == 'Y'):
                    return "EXIT$"
            else:
                print("[INVALID] :: Invalid input. Please try again")
                continue

        phoneFlag = True
        while (phoneFlag):
            user_response = input("[INPUT] :: Would you like to update User's Phone number ? [Y] Yes | [N] No  [E$] Exit :: ")
            if (user_response == 'Y'):
                user_response = input("[INPUT] :: Please enter the new Phone Number :: ")
                if (user_response == None or user_response.strip() == ""):
                    print("[EMPTY] :: Null/Empty input. Please try again")
                    continue
                elif (cVal.isPhoneValid(user_response) == False):
                    print("[INVALID] :: Not a valid Phone number. Please enter a valid one..")
                    continue
                else:
                    user_response = "\'" + user_response + "\'"
                    userUpdateInfoList.append([U_PHONE, user_response])
                    if DEBUG_MODE:
                        print("[DEBUG] :: Appending phone number update to the userUpdateInfoList")
                    phoneFlag = False
                    break
            elif user_response == 'N':
                break
            elif user_response == 'E$':
                user_response = input("[INPUT] :: Are you sure you want to Exit back to the Main menu without updating?? \n[Y] Yes | [N] No :: ")
                if (user_response == 'Y'):
                    return "EXIT$"
            else:
                print("[INVALID] :: Invalid input. Please try again")
                continue
    else:
        showMessagesToLibrarian(["[ERROR] :: User details could not be fetched before Updating"])
        return None

    if DEBUG_MODE:
        print("[DEBUG] :: Exiting fetchUserUpdateDetails().")
        print("[DEBUG] :: Returning the userUpdateInfoList :: ", userUpdateInfoList)
    return userUpdateInfoList


def fetchLibrarianUpdateDetails(current_user_name, current_user_regn_ID, librnObj:Librarian):
    '''This function fetches the Librarian account update related information details from Librarian
            @param current user name
            @:param current_user_regn_ID (to check & allow if the current Librarian wants to change own password)
            @:param Librarian object
            @:return List of Librarian's update details'''

    if DEBUG_MODE:
        print("[DEBUG] :: In fetchLibrarianUpdateDetails().")

    librns = "Librarian's"

    if (current_user_regn_ID != None and current_user_regn_ID == librnObj.get_l_regn_num()):
        librns = "Your"

    print(f"Hello, {current_user_name}! \n\tYou have chosen to update {librns} Account information ")
    print("--------------------------------------------------------------------")

    librnUpdateInfoList = []

    if (librnObj != None):
        print(f"\n{librns} details are as follows :: ")
        print(f"{librns} Registration ID :: ", librnObj.get_l_regn_num())
        print("---------------------------------------------")
        print(f"{librns} Name :: ", librnObj.get_l_name())
        print(f"{librns} Address :: ", librnObj.get_l_address())
        print(f"{librns} Email :: ", librnObj.get_l_email())
        print(f"{librns} Phone # :: ", librnObj.get_l_phone())
        print("---------------------------------------------")

        nameFlag = True
        while (nameFlag):
            librn_response = input(f"[INPUT] :: Would you like to update {librns} Display Name ? "
                                   f"[Y] Yes | [N] No  [E$] Exit :: ")
            if (librn_response == 'Y'):
                librn_response = input("[INPUT] :: Please enter the new Display Name :: ")
                if (librn_response == None or librn_response.strip() == ""):
                    print("[EMPTY] :: Null/Empty input. Please try again")
                    continue
                elif ("'" in librn_response):
                    print("[INVALID] :: Invalid input. Single quote ' character not valid in a Name. Try again.")
                    continue
                else:
                    librn_response = "\'" + librn_response + "\'"
                    librnUpdateInfoList.append([L_NAME, librn_response])
                    nameFlag = False
                    break
            elif librn_response == 'N':
                break
            elif librn_response == 'E$':
                librn_response = input(
                    "[INPUT] :: Are you sure you want to Exit back to the Main menu without updating?? \n[Y] Yes | [N] No :: ")
                if (librn_response == 'Y'):
                    return "EXIT$"
            else:
                print("[INVALID] :: Invalid input. Please try again")
                continue

        if (current_user_regn_ID != None and current_user_regn_ID == librnObj.get_l_regn_num()):
            pwdFlag = True
            while (pwdFlag):
                librn_response = input(
                    "[INPUT] :: Would you like to update your Password ? [Y] Yes | [N] No  [E$] Exit :: ")
                if (librn_response == 'Y'):
                    librn_response = input("[INPUT] :: Please enter the current Password :: ")
                    if (librn_response == None or librn_response.strip() == ""):
                        print("[EMPTY] :: Null/Empty input. Please try again")
                        continue
                    elif (librn_response == librnObj.get_l_pwd()):
                        librn_response = input("[INPUT] :: Please enter the new Password :: ")
                        if (librn_response == None or librn_response.strip() == ""):
                            print("[EMPTY] :: Null/Empty input. Please try again")
                            continue
                        elif (librn_response in KEYWORDSLIST):
                            print("[INVALID] :: Some Keywords are restricted from being set as passwords.")
                            print("Please try again.")
                            continue
                        elif ("'" in librn_response):
                            print(
                                "[INVALID] :: Invalid input. Single quote ' character not valid in a password. Try again.")
                            continue
                        else:
                            librn_response = "\'" + librn_response + "\'"
                            librnUpdateInfoList.append([L_PWD, librn_response])
                            pwdFlag = False
                            break
                    else:
                        print("[INVALID] :: Wrong password entered. Please enter the current password & try again..")
                        continue
                elif librn_response == 'N':
                    break
                elif librn_response == 'E$':
                    librn_response = input(
                        "[INPUT] :: Are you sure you want to Exit back to the Main menu without updating?? \n[Y] Yes | [N] No :: ")
                    if (librn_response == 'Y'):
                        return "EXIT$"
                else:
                    print("[INVALID] :: Invalid input. Please try again")
                    continue

        addressFlag = True
        while (addressFlag):
            librn_response = input(f"[INPUT] :: Would you like to update {librns} Address ? "
                                   f"[Y] Yes | [N] No  [E$] Exit :: ")
            if (librn_response == 'Y'):
                librn_response = input("[INPUT] :: Please enter the new Address information :: ")
                if (librn_response == None or librn_response.strip() == ""):
                    print("[EMPTY] :: Null/Empty input. Please try again")
                    continue
                else:
                    librn_response = librn_response.replace("'", "''")
                    librn_response = "\'" + librn_response + "\'"
                    librnUpdateInfoList.append([L_ADDRESS, librn_response])
                    addressFlag = False
                    break
            elif librn_response == 'N':
                break
            elif librn_response == 'E$':
                librn_response = input(
                    "[INPUT] :: Are you sure you want to Exit back to the Main menu without updating?? \n[Y] Yes | [N] No :: ")
                if (librn_response == 'Y'):
                    return "EXIT$"
            else:
                print("[INVALID] :: Invalid input. Please try again")
                continue

        emailFlag = True
        while (emailFlag):
            librn_response = input(f"[INPUT] :: Would you like to update {librns} E-Mail ID ? "
                                   f"[Y] Yes | [N] No  [E$] Exit :: ")
            if (librn_response == 'Y'):
                librn_response = input("[INPUT] :: Please enter the new E-Mail ID :: ")
                if (librn_response == None or librn_response.strip() == ""):
                    print("[EMPTY] :: Null/Empty input. Please try again")
                    continue
                elif (cVal.isEmailValid(librn_response) == False):
                    print("[INVALID] :: Not a valid E-Mail ID. Please enter a valid one..")
                    continue
                else:
                    librn_response = "\'" + librn_response + "\'"
                    librnUpdateInfoList.append([L_EMAIL, librn_response])
                    if DEBUG_MODE:
                        print("[DEBUG] :: Appending email update to the userUpdateInfoList")
                    emailFlag = False
                    break
            elif librn_response == 'N':
                break
            elif librn_response == 'E$':
                librn_response = input(
                    "[INPUT] :: Are you sure you want to Exit back to the Main menu without updating?? \n[Y] Yes | [N] No :: ")
                if (librn_response == 'Y'):
                    return "EXIT$"
            else:
                print("[INVALID] :: Invalid input. Please try again")
                continue

        phoneFlag = True
        while (phoneFlag):
            librn_response = input(f"[INPUT] :: Would you like to update {librns} Phone number ? "
                                   f"[Y] Yes | [N] No  [E$] Exit :: ")
            if (librn_response == 'Y'):
                librn_response = input("[INPUT] :: Please enter the new Phone Number :: ")
                if (librn_response == None or librn_response.strip() == ""):
                    print("[EMPTY] :: Null/Empty input. Please try again")
                    continue
                elif (cVal.isPhoneValid(librn_response) == False):
                    print("[INVALID] :: Not a valid Phone number. Please enter a valid one..")
                    continue
                else:
                    librn_response = "\'" + librn_response + "\'"
                    librnUpdateInfoList.append([L_PHONE, librn_response])
                    if DEBUG_MODE:
                        print("[DEBUG] :: Appending phone number update to the userUpdateInfoList")
                    phoneFlag = False
                    break
            elif librn_response == 'N':
                break
            elif librn_response == 'E$':
                librn_response = input(
                    "[INPUT] :: Are you sure you want to Exit back to the Main menu without updating?? \n[Y] Yes | [N] No :: ")
                if (librn_response == 'Y'):
                    return "EXIT$"
            else:
                print("[INVALID] :: Invalid input. Please try again")
                continue
    else:
        showMessagesToLibrarian(["[ERROR] :: Librarian details could not be fetched before Updating"])
        return None

    if DEBUG_MODE:
        print("[DEBUG] :: Exiting fetchLibrarianUpdateDetails().")
        print("[DEBUG] :: Returning the librnUpdateInfoList :: ", librnUpdateInfoList)
    return librnUpdateInfoList