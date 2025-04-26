# Storage/file_storage.py

import os
import shutil
from Models.file import File

class FileStorage:
    def __init__(self, base_dir='data'):
        """Base pour stocker les fichiers : dossier 'data'."""
        self.base_dir = os.path.abspath(base_dir)  # <- correction ici : chemin absolu
        os.makedirs(self.base_dir, exist_ok=True)

    def _user_dir(self, user):
        """Chemin complet du répertoire utilisateur."""
        user_dir = os.path.join(self.base_dir, user.user_id)
        os.makedirs(user_dir, exist_ok=True)
        return user_dir

    def save_file(self, user, file):
        """Sauvegarde un fichier uploadé par un utilisateur."""
        user_dir = self._user_dir(user)
        dest = os.path.join(user_dir, os.path.basename(file.path))
        shutil.copy2(file.path, dest)

    def get_file(self, user, file_name) -> File:
        """Retourne un fichier appartenant à un utilisateur."""
        full_path = os.path.join(self._user_dir(user), file_name)
        if os.path.exists(full_path):
            return File(full_path)
        else:
            raise FileNotFoundError(f"{file_name} not found for user {user.user_id}")

    def delete_file(self, user, file_name):
        """Supprime un fichier spécifique."""
        full_path = os.path.join(self._user_dir(user), file_name)
        if os.path.exists(full_path):
            os.remove(full_path)
