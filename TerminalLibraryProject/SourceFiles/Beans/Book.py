# Book.py

class Book:

    def __init__(self, bk_ID, bk_Code, bk_name, bk_author, bk_publication, bk_category, bk_fee,
                 bk_issuedBy, bk_issuedTo, bk_issuedDate, bk_availabilityStatus):
        self.bk_ID = bk_ID
        self.bk_Code = bk_Code
        self.bk_name = bk_name
        self.bk_author = bk_author
        self.bk_publication = bk_publication
        self.bk_category = bk_category
        self.bk_fee = bk_fee
        self.bk_issuedBy = bk_issuedBy
        self.bk_issuedTo = bk_issuedTo
        self.bk_issuedDate = bk_issuedDate
        self.bk_availabilityStatus = bk_availabilityStatus

    def __init__(self, bk_tpl):
        self.bk_ID = bk_tpl[0]
        self.bk_Code = bk_tpl[1]
        self.bk_name = bk_tpl[2]
        self.bk_author = bk_tpl[3]
        self.bk_publication = bk_tpl[4]
        self.bk_category = bk_tpl[5]
        self.bk_fee = bk_tpl[6]
        self.bk_issuedBy = bk_tpl[7]
        self.bk_issuedTo = bk_tpl[8]
        self.bk_issuedDate = bk_tpl[9]
        self.bk_availabilityStatus = bk_tpl[10]

    def set_bk_ID(self, bk_ID):
        self.bk_ID = bk_ID

    def get_bk_ID(self):
        return self.bk_ID

    def set_bk_Code(self, bk_Code):
        self.bk_Code = bk_Code

    def get_bk_Code(self):
        return self.bk_Code

    def set_bk_name(self, bk_name):
        self.bk_name = bk_name

    def get_bk_name(self):
        return self.bk_name

    def set_bk_author(self, bk_author):
        self.bk_author = bk_author

    def get_bk_author(self):
        return self.bk_author

    def set_bk_publication(self, bk_publication):
        self.bk_publication = bk_publication

    def get_bk_publication(self):
        return self.bk_publication

    def set_bk_category(self, bk_category):
        self.bk_category = bk_category

    def get_bk_category(self):
        return self.bk_category

    def set_bk_fee(self, bk_fee):
        self.bk_fee = bk_fee

    def get_bk_fee(self):
        return self.bk_fee

    def set_bk_issuedBy(self, bk_issuedBy):
        self.bk_issuedBy = bk_issuedBy

    def get_bk_issuedBy(self):
        return self.bk_issuedBy

    def set_bk_issuedTo(self, bk_issuedTo):
        self.bk_issuedTo = bk_issuedTo

    def get_bk_issuedTo(self):
        return self.bk_issuedTo

    def set_bk_issuedDate(self, bk_issuedDate):
        self.bk_issuedDate = bk_issuedDate

    def get_bk_issuedDate(self):
        return self.bk_issuedDate

    def set_bk_availabilityStatus(self, bk_availabilityStatus):
        self.bk_availabilityStatus = bk_availabilityStatus

    def get_bk_availabilityStatus(self):
        return self.bk_availabilityStatus

    ### Method that returns Book object in the form of a dictionary element having Book ID number as KEY
    ### and all BOOK Info as a value containing list object
    def getBookInfoDict(self):
        return {self.bk_Code: [self.bk_ID, self.bk_Code, self.bk_name, self.bk_author, self.bk_publication,
                               self.bk_category,
                               self.bk_fee, self.bk_issuedBy, self.bk_issuedTo, self.bk_issuedDate,
                               self.bk_availabilityStatus]}

    ### Method that sets Book object to null object
    def setBookToNull(self):
        self.bk_ID = 0
        self.bk_Code = ""
        self.bk_name = ""
        self.bk_author = ""
        self.bk_publication = ""
        self.bk_category = ""
        self.bk_fee = ""
        self.bk_issuedBy = ""
        self.bk_issuedTo = ""
        self.bk_issuedDate = ""
        self.bk_availabilityStatus = ""
