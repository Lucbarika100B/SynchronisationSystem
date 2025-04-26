import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class UserManager:
    def __init__(self):
        self.users = {}  # {username: User}

    def add_user(self, user: User):
        self.users[user.user_id] = user

    def get_user(self, user_id: str):
        return self.users.get(user_id)

    def is_authenticated(self, user_id: str):
        user = self.users.get(user_id)
        return user.is_authenticated() if user else False
