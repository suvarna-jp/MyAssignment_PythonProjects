# User.py

class User:

    # def __init__(self, u_ID, u_regnNum, u_pwd, u_name, u_address, u_email, u_phone):
    #     self.u_ID = u_ID
    #     self.u_regn_num = u_regnNum
    #     self.u_pwd = u_pwd
    #     self.u_name = u_name
    #     self.u_address = u_address
    #     self.u_email = u_email
    #     self.u_phone = u_phone

    def __init__(self, validUser):
        self.u_ID = validUser[0]
        self.u_regn_num = validUser[1]
        self.u_pwd = validUser[2]
        self.u_name = validUser[3]
        self.u_address = validUser[4]
        self.u_email = validUser[5]
        self.u_phone = validUser[6]

    def set_u_ID(self, u_ID):
        self.u_ID = u_ID

    def get_u_ID(self):
        return self.u_ID

    def set_u_regn_num(self, u_regn_num):
        self.u_regn_num = u_regn_num

    def get_u_regn_num(self):
        return self.u_regn_num

    def set_u_pwd(self, u_pwd):
        self.u_pwd = u_pwd

    def get_u_pwd(self):
        return self.u_pwd

    def set_u_name(self, u_name):
        self.u_name = u_name

    def get_u_name(self):
        return self.u_name

    def set_u_address(self, u_address):
        self.u_address = u_address

    def get_u_address(self):
        return self.u_address

    def set_u_email(self, u_email):
        self.u_email = u_email

    def get_u_email(self):
        return self.u_email

    def set_u_phone(self, u_phone):
        self.u_phone = u_phone

    def get_u_phone(self):
        return self.u_phone

    ### Method that returns User object in the form of a dictionary element having User Registration number as KEY
    ### and all User Info as a value containing list object
    def getUserInfoDict(self):
        return {self.u_regn_num: [self.u_ID, self.u_regn_num, self.u_pwd, self.u_name, self.u_address, self.u_email,
                                  self.u_phone]}

    ### Method that returns User object in the form of a dictionary element having User Registration number as KEY
    ### and all User Info as a value containing list object
    def getUserInfoList(self):
        return [self.u_ID, self.u_regn_num, self.u_pwd, self.u_name, self.u_address, self.u_email, self.u_phone]

