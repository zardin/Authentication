class User:
    def __init__(self, email, name, password, id):
        self.UserName = name
        self.Email = email
        self.Name = name
        self.Password = password
        self.id = id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)