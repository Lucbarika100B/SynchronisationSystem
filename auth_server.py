# Authentication/auth_server.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
import socket
import json
import threading
from Authentication.user_db import UserDB


class AuthServer:
    def __init__(self, ip='127.0.0.1', port=9999):
        self.server_ip = ip
        self.server_port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.server_ip, self.server_port))
        self.running = True

        # Utiliser UserDB
        self.user_db = UserDB()
        self.user_db.load_users()

        print(f"[INFO] AuthServer listening on {self.server_ip}:{self.server_port}")

    def start(self):
        print(f"[AUTH SERVER] En attente de connexions sur {self.server_ip}:{self.server_port}...\n")
        while self.running:
            try:
                data, addr = self.socket.recvfrom(4096)
                message = data.decode('utf-8')
                print(f"[REÇU] {addr} : {message}")
                threading.Thread(target=self.handle_request, args=(message, addr)).start()
            except Exception as e:
                print(f"[ERREUR] {e}")

    def handle_request(self, message, addr):
        try:
            request = json.loads(message)
            action = request.get("action")
            username = request.get("username")
            password = request.get("password")

            if action == "login":
                self.handle_login(username, password, addr)
            elif action == "logout":
                self.handle_logout(username, addr)
            elif action == "shutdown":
                self.handle_shutdown(username, password, addr)
            elif action == "list_users":
                self.handle_list_users(username, password, addr)
            else:
                self.send_response(addr, {"status": "error", "message": "Action inconnue."})
        except json.JSONDecodeError:
            self.send_response(addr, {"status": "error", "message": "Message JSON invalide."})

    def handle_login(self, username, password, addr):
        if self.user_db.validate(username, password):
            print(f"[CONNEXION] {username} connecté depuis {addr[0]}")
            self.send_response(addr, {"status": "success", "message": "Login réussi"})
            try:
                requests.post("http://127.0.0.1:5000/connect_user", json={"user": username})
            except Exception as e:
                print(f"[REST NOTIFY] Erreur : {e}")
        else:
            print(f"[ÉCHEC] Tentative de login invalide de {addr}")
            self.send_response(addr, {"status": "fail", "message": "Identifiants invalides"})

    def handle_logout(self, username, addr):
        # Pas besoin de mot de passe pour logout
        print(f"[DÉCONNEXION] {username}")
        self.send_response(addr, {"status": "success", "message": "Logout réussi"})

    def handle_shutdown(self, username, password, addr):
        if username == "admin" and self.user_db.validate(username, password):
            self.running = False
            print("[SHUTDOWN] Serveur arrêté par l’admin.")
            self.send_response(addr, {"status": "success", "message": "Serveur arrêté."})
        else:
            self.send_response(addr, {"status": "fail", "message": "Accès refusé"})

    def handle_list_users(self, username, password, addr):
        if username == "admin" and self.user_db.validate(username, password):
            # (Tu peux ajouter une vraie liste si tu veux aller plus loin)
            self.send_response(addr, {"status": "success", "message": "Liste non implémentée ici."})
        else:
            self.send_response(addr, {"status": "fail", "message": "Accès refusé"})

    def send_response(self, addr, response):
        response_data = json.dumps(response).encode('utf-8')
        self.socket.sendto(response_data, addr)

# Point d’entrée
if __name__ == "__main__":
    server = AuthServer()
    server.start()
