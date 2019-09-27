# LoginPageView.py


### Reads login ID /Registration ID from the end user
### @Returns : login/registration ID
def getLoginID():
    print("[MESSAGE] :: [If you want to Exit this app, enter \"EXIT$\"]")
    loginRegnID = input("[INPUT] :: Please enter your Login ID/Registration ID : ")
    return loginRegnID


### Reads the password from the end user
### @Returns : password
### @Returns : "F$P$" - in case end user has forgotten password (This invokes 'forgotPassword()' function)
def getPassword():
    print("[MESSAGE] :: [If you have forgotten password, enter \"F$P$\"]")
    pwd = input("[INPUT] :: Please enter your password : ")
    if pwd == "F$P$":
        forgotPassword()
        return "F$P$"
    else:
        return pwd


### Functionality is yet to be implemented. Until then, just redirecting end user to Login page
### @Returns : "F$P$" - to show end user has forgotten password
def forgotPassword():
    # bday = input("Please enter your Birthday in format (yyyy-mm-dd) : ")
    print("[MESSAGE] :: This functionality could have validated birthdate from user and could have sent a mail.")
    print("[MESSAGE] :: This functionality is yet to be implemented. Sorry for the inconvenience!!")
    print("[MESSAGE] :: Please approach a Librarian/Admin for help...")
    print("[MESSAGE] :: Redirecting to Login page again...")
    print("[MESSAGE] :: Thank you for using Terminal Library App!!")
    return "F$P$"


### Prints a message to the end user before logout
### @Args : username (String)
def logout(username):
    print(f"[MESSAGE] :: Dear {username}!! Thank you for using Terminal Library App!!")
    return "LOGOUT$"
