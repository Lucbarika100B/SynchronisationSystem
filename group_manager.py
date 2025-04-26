import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class GroupManager:
    def __init__(self):
        self.groups = {}  # {folder_name: [user_id]}

    def create_group(self, folder_name: str, admin: str):
        self.groups[folder_name] = [admin]

    def add_user_to_group(self, folder_name: str, user_id: str):
        if folder_name in self.groups:
            if user_id not in self.groups[folder_name]:
                self.groups[folder_name].append(user_id)

    def remove_user_from_group(self, folder_name: str, user_id: str):
        if folder_name in self.groups and user_id in self.groups[folder_name]:
            self.groups[folder_name].remove(user_id)

    def get_users_in_group(self, folder_name: str):
        return self.groups.get(folder_name, [])
