# Librarian.py

class Librarian:

    # def __init__(self, l_ID, l_regnNum, l_pwd, l_name, l_address, l_email, l_phone):
    #     self.l_ID = l_ID
    #     self.l_regnNum = l_regnNum
    #     self.l_pwd = l_pwd
    #     self.l_name = l_name
    #     self.l_address = l_address
    #     self.l_email = l_email
    #     self.l_phone = l_phone

    def __init__(self, validLibrarian):
        self.l_ID = validLibrarian[0]
        self.l_regn_num = validLibrarian[1]
        self.l_pwd = validLibrarian[2]
        self.l_name = validLibrarian[3]
        self.l_address = validLibrarian[4]
        self.l_email = validLibrarian[5]
        self.l_phone = validLibrarian[6]

    def set_l_ID(self, l_ID):
        self.l_ID = l_ID

    def get_l_ID(self):
        return self.l_ID

    def set_l_regn_num(self, l_regn_num):
        self.l_regn_num = l_regn_num

    def get_l_regn_num(self):
        return self.l_regn_num

    def set_l_pwd(self, l_pwd):
        self.l_pwd = l_pwd

    def get_l_pwd(self):
        return self.l_pwd

    def set_l_name(self, l_name):
        self.l_name = l_name

    def get_l_name(self):
        return self.l_name

    def set_l_address(self, l_address):
        self.l_address = l_address

    def get_l_address(self):
        return self.l_address

    def set_l_email(self, l_email):
        self.l_email = l_email

    def get_l_email(self):
        return self.l_email

    def set_l_phone(self, l_phone):
        self.l_phone = l_phone

    def get_l_phone(self):
        return self.l_phone

    ### Method that returns Librarian object in the form of a dictionary element having Librarian Registration number as KEY
    ### and all Librarian Info as a value containing list object
    def getLibrarianInfoDict(self):
        return {self.l_regn_num: [self.l_ID, self.l_regn_num, self.l_pwd, self.l_name, self.l_address, self.l_email,
                                  self.l_phone]}

    ### Method that returns Librarian object in the form of a dictionary element having Librarian Registration number as KEY
    ### and all Librarian Info as a value containing list object
    def setLibrarianToNull(self):
        self.l_ID = 0
        self.l_regn_num = ""
        self.l_pwd = ""
        self.l_name = ""
        self.l_address = ""
        self.l_email = ""
        self.l_phone = ""
