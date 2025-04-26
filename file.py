# Models/file.py
import hashlib
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class File:
    def __init__(self, path):
        self.path = path

    def get_checksum(self) -> str:
        with open(self.path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()

    def is_modified_since(self, timestamp: float) -> bool:
        return os.path.getmtime(self.path) > timestamp
