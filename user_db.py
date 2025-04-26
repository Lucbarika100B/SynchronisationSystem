# Authentication/user_db.py

from werkzeug.security import generate_password_hash, check_password_hash

class UserDB:
    def __init__(self):
        """Initialise la base de données simulée des utilisateurs."""
        # Dictionnaire simulé {username: mot_de_passe_haché}
        self.users = {}

    def load_users(self):
        """Charge des utilisateurs fictifs dans la base."""
        self.users["user1"] = generate_password_hash("pass1")
        self.users["user2"] = generate_password_hash("pass2")
        self.users["admin"] = generate_password_hash("root")

    def validate(self, username: str, password: str) -> bool:
        """
        Valide un utilisateur : vérifie que le nom d'utilisateur existe
        et que le mot de passe est correct.
        """
        if username in self.users and check_password_hash(self.users[username], password):
            return True
        return False

    def remove_user(self, username: str):
        """Supprime un utilisateur de la base."""
        if username in self.users:
            del self.users[username]
            print(f"[INFO] Utilisateur {username} supprimé.")
        else:
            print(f"[WARN] Utilisateur {username} non trouvé.")
