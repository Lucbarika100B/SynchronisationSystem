# Models/folder.py
import os
from Models.file import File
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Folder:
    def __init__(self, path):
        self.path = path
        self.shared_with = []

    def remove_file(self, file_name: str):
        file_path = os.path.join(self.path, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)

    def share_with(self, user):
        if user not in self.shared_with:
            self.shared_with.append(user)

    def list_files(self) -> list[str]:
        return [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
