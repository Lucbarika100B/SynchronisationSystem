import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pathlib import Path
import shutil
from filecmp import cmp

class SyncService:
    def compare_local_remote(self, local: Path, remote: Path) -> Path:
        """
        Compare les fichiers local et distant et retourne celui qui est le plus récent (basé sur date de modification).
        """
        if not local.exists() or not remote.exists():
            return local if local.exists() else remote

        local_mtime = os.path.getmtime(local)
        remote_mtime = os.path.getmtime(remote)

        return local if local_mtime >= remote_mtime else remote

    def synch_user(self, user_folder: Path) -> None:
        """
        Synchronise les fichiers d'un utilisateur entre le dossier local et le dossier distant.
        """
        remote_folder = Path("server_storage") / user_folder.name
        remote_folder.mkdir(parents=True, exist_ok=True)

        for file in user_folder.glob("*"):
            remote_file = remote_folder / file.name

            latest = self.compare_local_remote(file, remote_file)
            if latest == file and not cmp(file, remote_file, shallow=False):
                shutil.copy2(file, remote_file)
            elif latest == remote_file and not cmp(file, remote_file, shallow=False):
                shutil.copy2(remote_file, file)

    def resolve_conflict(self, file1: Path, file2: Path) -> Path:
        """
        Résout un conflit de version entre deux fichiers, en gardant le plus récent.
        """
        return self.compare_local_remote(file1, file2)
