class User:

    def __init__(self, firstname, lastname, email, username, password,company_name):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.username = username
        self.password = password
        self.company_name = company_name

    def __str__(self):
        return self.username + self.password + self.email
    
    def getUsername(self):
        return self.username


    @staticmethod
    def searchUser(username, password):
        with open('userInfo.csv', 'r') as file:
            for line in file:
                fields = line.strip().split(",")
                if len(fields) == 6:
                    firstname, lastname, user_email, current_username, current_password, company_name = fields
                    if username == current_username and password == current_password:
                        return True
        return False
    
    @staticmethod
    def updateUser(username, password, email):
        with open('userInfo.csv', 'r') as file:
            for line in file:
                fields = line.strip().split(",")
                if len(fields) == 6:
                    firstname, lastname, email, current_username, current_password,company_name = fields
                    if username == current_username and password == current_password:
                        fields = [firstname, lastname, email, current_username, current_password]
                        print(fields)
                    return True
            return False # if return False then return message cant find
    
    def deleteUser(username, password):
        with open('userInfo.csv', 'r') as file:
            for line in file:
                fields = line.strip().split(",")
                if len(fields) == 6:
                    firstname, lastname, email, current_username, current_password,company_name = fields
                    currentUser = User(*fields)
                    if username == current_username and password == current_password:
                        del currentUser # use of deconstructor
        return False # if return False then return message cant find
    
    @staticmethod
    def createUser(firstname, lastname, email, current_username, current_password,company_name):
        with open('userInfo.csv', 'a') as file: # append mode
            file.write(f"{firstname},{lastname},{email},{current_username},{current_password},{company_name}\n")