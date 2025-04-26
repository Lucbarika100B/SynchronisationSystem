# Models/user.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class User:
    def __init__(self, user_id, authenticated=False):
        self.user_id = user_id
        self.authenticated = authenticated
        self.shared_folders = []

    def is_authenticated(self) -> bool:
        return self.authenticated

    def get_shared_folders(self) -> list[str]:
        return self.shared_folders
