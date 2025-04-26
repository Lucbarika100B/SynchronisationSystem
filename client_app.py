import sys
import os
import socket
import json
import requests
from pathlib import Path

# Ajout du répertoire parent pour les imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class ClientApp:
    def __init__(self, username, password, udp_host='127.0.0.1', udp_port=9999, rest_url='http://127.0.0.1:5000'):
        self.username = username
        self.password = password
        self.udp_host = udp_host
        self.udp_port = udp_port
        self.rest_url = rest_url
        self.base_folder = Path("IFT585-TP") / self.username
        self.base_folder.mkdir(parents=True, exist_ok=True)

    def authenticate_udp(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        auth_data = {
            "action": "login",
            "username": self.username,
            "password": self.password
        }
        sock.sendto(json.dumps(auth_data).encode(), (self.udp_host, self.udp_port))

        try:
            response, _ = sock.recvfrom(1024)
            decoded = json.loads(response.decode())
            print(f"[AUTH UDP] Réponse du serveur : {decoded}")
        except Exception as e:
            print(f"[AUTH UDP] Erreur de réception : {e}")
        finally:
            sock.close()

    def sync_rest(self):
        try:
            res = requests.post(f"{self.rest_url}/sync", json={"user": self.username})
            print(f"[SYNC] Synchronisation : {res.json()}")
        except Exception as e:
            print(f"[SYNC] Erreur : {e}")

    def upload(self, file_path, folder_name=None):
        path = Path(file_path)
        if not path.exists():
            print("[UPLOAD] Fichier introuvable")
            return

        files = {'file': open(path, 'rb')}
        data = {'user': self.username}
        if folder_name:
            data['folder'] = folder_name

        try:
            res = requests.post(f"{self.rest_url}/upload", files=files, data=data)
            print(f"[UPLOAD] Réponse : {res.json()}")
        except Exception as e:
            print(f"[UPLOAD] Échec : {e}")

    def download(self, file_name, folder_name=None):
        try:
            if folder_name:
                remote_file_path = f"{folder_name}/{file_name}"
            else:
                remote_file_path = file_name

            res = requests.get(f"{self.rest_url}/download", params={"user": self.username, "filename": remote_file_path})
            if res.status_code == 200:
                # Correction ici : Sauver dans local dossier IFT585-TP/username/dossier_test/
                save_folder = self.base_folder
                if folder_name:
                    save_folder = save_folder / folder_name
                    save_folder.mkdir(parents=True, exist_ok=True)

                local_path = save_folder / file_name
                with open(local_path, 'wb') as f:
                    f.write(res.content)
                print(f"[DOWNLOAD] Fichier sauvegardé : {local_path}")
            else:
                print(f"[DOWNLOAD] Échec : {res.text}")
        except Exception as e:
            print(f"[DOWNLOAD] Erreur : {e}")

    def create_folder(self, name):
        try:
            res = requests.post(f"{self.rest_url}/create_folder", json={
                "user": self.username,
                "folder": name
            })
            print(f"[CREATE] Réponse : {res.json()}")
        except Exception as e:
            print(f"[CREATE] Erreur : {e}")

    def invite_user(self, user, folder):
        try:
            res = requests.post(f"{self.rest_url}/invite", json={
                "owner": self.username,
                "invitee": user,
                "folder": folder
            })
            print(f"[INVITE] Réponse : {res.json()}")
        except Exception as e:
            print(f"[INVITE] Erreur : {e}")

    def run_all(self):
        self.authenticate_udp()
        self.create_folder("dossier_test")
        self.upload("testfile.pdf", folder_name="dossier_test")
        self.sync_rest()
        self.download("testfile.pdf", folder_name="dossier_test")
        self.invite_user("user2", "dossier_test")


if __name__ == "__main__":
    client = ClientApp("user1", "pass1")
    client.run_all()
