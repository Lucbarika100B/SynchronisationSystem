import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class ShareService:
    def __init__(self):
        self.shared_folders = {}  # (owner, folder) → set of invited usernames

    def invite_user(self, owner: str, invitee: str, folder: str) -> bool:
        """
        Invite un utilisateur à collaborer sur un dossier.
        """
        key = (owner, folder)
        if key not in self.shared_folders:
            self.shared_folders[key] = set()
        self.shared_folders[key].add(invitee)
        return True

    def revoke_access(self, owner: str, invitee: str, folder: str) -> bool:
        """
        Révoque les droits d'accès d'un utilisateur à un dossier.
        """
        key = (owner, folder)
        if key in self.shared_folders and invitee in self.shared_folders[key]:
            self.shared_folders[key].remove(invitee)
            return True
        return False
