# AdminPageView.py


# Reads option from Admin
def showAdminOptions():
    print("[A] : Perform all Admin operations for first time use.")
    print("[B] : Create Basic Tables in DB")
    print("[C] : Populate Test entries in Tables in DB")
    print("[D] : Delete Test entries in Tables in DB")
    print("[STRICT$] : Strictly for testing purpose, change book issue date ")
    print("[E] : Logout")

    admin_option = input("\nPlease enter an option :: ")
    return admin_option
