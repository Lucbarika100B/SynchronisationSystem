# Server/rest_server.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify, send_file
from Storage.file_storage import FileStorage
from Models.user import User
from Models.file import File
from Models.folder import Folder

app = Flask(__name__)
file_storage = FileStorage()
connected_users = {}  # Session simulée

@app.route("/connect_user", methods=["POST"])
def connect_user():
    username = request.json.get("user")
    user = User(username, authenticated=True)
    connected_users[username] = user
    print(f"[REST] Utilisateur {username} connecté")
    return jsonify({"status": "success"})

@app.route("/upload", methods=["POST"])
def upload():
    username = request.form.get("user")
    user = connected_users.get(username)
    if not user:
        return jsonify({"status": "fail", "message": "Utilisateur non authentifié"})

    file = request.files["file"]
    temp_path = os.path.join("temp", file.filename)
    os.makedirs("temp", exist_ok=True)
    file.save(temp_path)
    file_storage.save_file(user, File(temp_path))
    os.remove(temp_path)

    return jsonify({"status": "success", "message": "Fichier uploadé avec succès"})

@app.route("/download", methods=["GET"])
def download():
    username = request.args.get("user")
    filename = request.args.get("filename")
    user = connected_users.get(username)
    if not user:
        return "Utilisateur non authentifié", 403

    try:
        # Correction IMPORTANTE : chercher dans data/user1/
        full_path = os.path.join(file_storage._user_dir(user), filename)
        if os.path.exists(full_path):
            return send_file(full_path, as_attachment=True)
        else:
            return "Fichier introuvable", 404
    except Exception as e:
        print(f"[REST][ERREUR] {e}")
        return "Erreur serveur", 500

@app.route("/sync", methods=["POST"])
def sync():
    username = request.json.get("user")
    user = connected_users.get(username)
    if not user:
        return jsonify({"status": "fail", "message": "Utilisateur non connecté"})

    try:
        file_list = os.listdir(file_storage._user_dir(user))
        return jsonify({"status": "success", "files": file_list})
    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)})

@app.route("/create_folder", methods=["POST"])
def create_folder():
    username = request.json.get("user")
    folder = request.json.get("folder")
    user = connected_users.get(username)
    if not user:
        return jsonify({"status": "fail", "message": "Utilisateur non connecté"})

    path = os.path.join(file_storage._user_dir(user), folder)
    os.makedirs(path, exist_ok=True)
    return jsonify({"status": "success", "message": f"Dossier {folder} créé"})

@app.route("/invite", methods=["POST"])
def invite():
    owner = request.json.get("owner")
    invitee = request.json.get("invitee")
    folder = request.json.get("folder")
    user = connected_users.get(owner)
    if not user:
        return jsonify({"status": "fail", "message": "Utilisateur non connecté"})

    folder_path = os.path.join(file_storage._user_dir(user), folder)
    shared_folder = Folder(folder_path)
    shared_folder.share_with(invitee)
    return jsonify({"status": "success", "message": f"{invitee} invité à {folder}"})

if __name__ == "__main__":
    app.run(debug=True)
