class AuthManager:
    def __init__(self):
        self.users = {
            'carlossanabria': '1234',
            'johancholes': '0000'
        }
        
    def authenticate(self, username, password):
        return self.users.get(username) == password
