# CommonValidations.py
import re
from SourceFiles.Commons.CommonIncludes import DEBUG_MODE

# DEBUG_MODE = False

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

def rectifyRestrictedSpecialCharacters(stringValue):
    '''Checks if the string value contains a single quote which is a restricted value while entering the details.'''
    if(stringValue != None and "'" in stringValue):
        newString = ""
        for quote in stringValue:
            if quote == "'":
                print(quote)
                quote = "''"
            newString += quote
        if DEBUG_MODE:
            print("\n", stringValue, " changed to newString :: ", newString, "\n")
        return newString
    else:
        return stringValue

