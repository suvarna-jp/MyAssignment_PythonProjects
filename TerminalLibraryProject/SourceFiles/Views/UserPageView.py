# UserPageView.py

import re

from SourceFiles.Beans import User
from SourceFiles.Beans.User import User
from SourceFiles.Commons.CommonIncludes import DEBUG_MODE

# # Global variable for Debug statements
# DEBUG_MODE = False

# Some Keywords that cannot be used as like setting passwords, etc
KEYWORDSLIST = ['F$P$', 'admin$', 'EXIT$, LOGOUT$']

# Database User table column names
# Dynamic assignment to prepare the query
U_NAME = 'user_Name'
U_PWD = 'user_Password'
U_ADDRESS = 'user_Address'
U_EMAIL = 'user_EMail'
U_PHONE = 'user_Phone'


def showUserOptions(username):
    '''Reads options from User
    @:param Username - Just to show a customized message'''

    print(f"\nDear {username}! Choose an option from the below list : ")
    print("--------------------------------------")

    print("[A] : View Available Books in the Library")
    print("[B] : View Book details")
    print("[C] : View the total amount to be paid by me")
    print("[D] : View my account details")
    print("[E] : Update my account details")
    print("[L] : Logout")

    user_option = input("\n[INPUT] :: Please enter an option :: ")
    return user_option


def showUserAmountToBePaid(amountTpl):
    '''This function displays (Kind of a)
    Billing Details to User
    @:param A tuple with billing related details'''

    if(amountTpl != None and len(amountTpl) == 11):
        print("\n" + amountTpl[1] + "! Here is your billing info : ")
        print("========================================================================")
        print("User Registration Number :: ", amountTpl[0])
        print("User Name :: ", amountTpl[1])
        print("Book Code :: ", amountTpl[2])
        print("Book Name :: ", amountTpl[3])
        print("Book was Issued on :: ", amountTpl[4])
        print("Today's Date :: ", amountTpl[5])
        print("Number of days rented :: ", amountTpl[6])
        print("Fine applicable days :: ", amountTpl[7])

        print("\nBook Fee Amount for first 20 days :: ", amountTpl[8])
        print("Fine amount for the fine applicable days :: ", amountTpl[9])
        print("------------------------------------------------------------------------")
        print("Total Amount to be paid :: ", amountTpl[10])
        print("========================================================================")
        print("[Note ::  The fine amount is calculated based on the following. "
              "\nIf a book is rented out for more than 20 days, "
              "\nfine will be added to the user. "
              "\nThe fine will be cummulative after every 5 days after that."
              "\neg: After 20 days, the fine will be Rs. 20, after 5 days, "
              "\nit will be 20+25, after another 5 days it will be 20+25+30.]")
        print("========================================================================")
        print("\n")

    else:
        print("Unexpected | Amount Object empty or invalid.")


def notifyUser(amountTpl):
    '''This function displays (Kind of a)
    Billing Details to User
    @:param A tuple with billing related details'''

    if DEBUG_MODE:
        print(f"[DEBUG] :: In notifyUser() amountTpl :: {amountTpl}")

    if(amountTpl != None and len(amountTpl) == 11 and type(amountTpl[6]) == int and amountTpl[6] > 14):

        daysToReturnBook = 0
        if (type(amountTpl[6]) == int and amountTpl[6] <= 20 and amountTpl[6] > 14):
            daysToReturnBook = 20 - amountTpl[6]
            showMessagesToUser([f"\n[TODAY's NOTIFICATION] :: Dear {amountTpl[1]}! ",
                                f"You have {daysToReturnBook} day(s) to return the book ",
                                "---------------------------------------------------------------------------",
                                f"{amountTpl[2]} :: {amountTpl[3]} ",
                                f"without any fine amount applicable",
                                f"Book Fee Amount for first 20 days :: {amountTpl[8]}",
                                "---------------------------------------------------------------------------",
                                f"Total Amount to be paid (if you return the book today) :: {amountTpl[10]}",
                                "==========================================================================="])
        elif(type(amountTpl[6]) == int and amountTpl[6] > 20):
            daysToReturnBook = amountTpl[6] - 20
            showMessagesToUser([f"\n[TODAY's NOTIFICATION] :: Dear {amountTpl[1]}! ",
                                f"You have exceeded {daysToReturnBook} day(s) to return the book ",
                                "---------------------------------------------------------------------------",
                                f"{amountTpl[2]} :: {amountTpl[3]} ",
                                f"The fine amount applicable, ",
                                f"if you would return the book today would be :: {amountTpl[9]}",
                                f"Book Fee Amount for first 20 days :: {amountTpl[8]}",
                                "---------------------------------------------------------------------------",
                                f"Total Amount to be paid (if you return the book today) :: {amountTpl[10]}",
                                "==========================================================================="])
    else:
        if DEBUG_MODE:
            print("[ERROR] :: Unexpected | Amount Object empty or invalid. In notifyUser()")



def fetchUserUpdateDetails(user:User):
    '''This function fetches the User account update related information details from  User
        @param current User object'''

    if DEBUG_MODE:
        print("[DEBUG] :: In fetchUserUpdateDetails().")

    print(f"Hello, {user.get_u_name()}! \n\tYou have chosen to update your User Account information ")
    print("--------------------------------------------------------------------")

    userUpdateInfoList = []

    nameFlag = True
    while (nameFlag):
        user_response = input("[INPUT] :: Would you like to update your Display Name ? [Y] Yes | [N] No  [E$] Exit :: ")
        if(user_response == 'Y'):
            user_response = input("[INPUT] :: Please enter the Display Name you would want to update to :: ")
            if(user_response == None or user_response.strip() == ""):
                print("[EMPTY] :: Null/Empty input. Please try again")
                continue
            elif("'" in user_response):
                print("[INVALID] :: Invalid input. Single quote character ' not valid in a Name. Please try again.")
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

    pwdFlag = True
    while (pwdFlag):
        user_response = input("[INPUT] :: Would you like to update your Password ? [Y] Yes | [N] No  [E$] Exit :: ")
        if (user_response == 'Y'):
            user_response = input("[INPUT] :: Please enter the new Password :: ")
            if (user_response == None or user_response.strip() == ""):
                print("[EMPTY] :: Null/Empty input. Please try again")
                continue
            elif(user_response in KEYWORDSLIST):
                print("[INVALID] :: Some Keywords are restricted from being set as passwords.")
                print("Please try again.")
                continue
            elif ("'" in user_response):
                print("[INVALID] :: Invalid input. Single quote character ' not valid in a password. Please try again.")
                continue
            else:
                user_response = "\'" + user_response + "\'"
                userUpdateInfoList.append([U_PWD, user_response])
                pwdFlag = False
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

    addressFlag = True
    while (addressFlag):
        user_response = input("[INPUT] :: Would you like to update your Address ? [Y] Yes | [N] No  [E$] Exit :: ")
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
        user_response = input("[INPUT] :: Would you like to update your E-Mail ID ? [Y] Yes | [N] No  [E$] Exit :: ")
        if (user_response == 'Y'):
            user_response = input("[INPUT] :: Please enter the new E-Mail ID :: ")
            if (user_response == None or user_response.strip() == ""):
                print("[EMPTY] :: Null/Empty input. Please try again")
                continue
            elif(isEmailValid(user_response) == False):
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
        user_response = input("[INPUT] :: Would you like to update your Phone number ? [Y] Yes | [N] No  [E$] Exit :: ")
        if (user_response == 'Y'):
            user_response = input("[INPUT] :: Please enter the new Phone Number :: ")
            if (user_response == None or user_response.strip() == ""):
                print("[EMPTY] :: Null/Empty input. Please try again")
                continue
            elif (isPhoneValid(user_response) == False):
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

    if DEBUG_MODE:
        print("[DEBUG] :: Exiting fetchUserUpdateDetails().")
        print("[DEBUG] :: Returning the userUpdateInfoList :: ", userUpdateInfoList)
    return userUpdateInfoList


def isEmailValid(email):
    '''Validates the EMail
        @:param EMail
        @:return 'True' if email is valid and 'False' otherwise.'''
    if len(email) > 7:
        if re.match("^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", email) != None:
            return True
    return False


def isPhoneValid(phone):
    '''Validates the phone number
        @:param phone number
        @:return 'True' if phone number is valid and 'False' otherwise.'''
    if(phone.isdigit() == False):
        return False

    for _ in range(int(phone)):

        if re.match(r"^[789]{1}\d{9}$", phone):
            return True
        else:
            return False


def showUserInformation(userObj:User):
    '''This function displays the User details
    to the user in a formatted pattern'''

    if DEBUG_MODE:
        print("[DEBUG] :: In showUserInformation().")

    if (userObj != None ):
        print("\n", userObj.get_u_name(), "'s Personal Account Information ")
        print("==========================================================")
        print("Registration Number :: ", userObj.get_u_regn_num())
        print("Name :: ", userObj.get_u_name())
        print("Email ID :: ", userObj.get_u_email())
        print("Phone # :: ", userObj.get_u_phone())
        print("Residential Address :: ", userObj.get_u_address())
        print("==========================================================")
    else:
        if DEBUG_MODE:
            print("[EMPTY] :: Null User object.")

    if DEBUG_MODE:
        print("[DEBUG] :: Exiting showUserInformation().")


def showMessagesToUser(msgsList):
    '''This function displays messages to the user
    @:param List - List of String messages'''

    if(msgsList != None and len(msgsList) > 0):
        for msg in msgsList:
            print(msg)
