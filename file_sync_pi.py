import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, jsonify, send_file
import os

class FileSyncAPI:
    def __init__(self, base_dir="IFT585-TP"):
        self.app = Flask(__name__)
        self.base_dir = base_dir
        self.setup_routes()

    def setup_routes(self):
        self.app.add_url_rule('/upload', 'upload', self.upload_file, methods=['POST'])
        self.app.add_url_rule('/download', 'download', self.download_file, methods=['GET'])
        self.app.add_url_rule('/status', 'status', self.sync_status, methods=['GET'])
        self.app.add_url_rule('/create_folder', 'create_folder', self.create_folder, methods=['POST'])
        self.app.add_url_rule('/invite', 'invite', self.invite_user_to_folder, methods=['POST'])

    def start_server(self):
        print("[+] Démarrage du serveur REST sur http://0.0.0.0:5000")
        self.app.run(host="0.0.0.0", port=5000)

    def upload_file(self):
        user_id = request.form.get("user_id")
        file = request.files.get("file")
        if not user_id or not file:
            return jsonify({"status": "error", "message": "Champs manquants"}), 400

        user_folder = os.path.join(self.base_dir, user_id)
        os.makedirs(user_folder, exist_ok=True)

        file_path = os.path.join(user_folder, file.filename)
        file.save(file_path)

        return jsonify({"status": "success", "message": f"Fichier {file.filename} téléversé"})

    def download_file(self):
        user_id = request.args.get("user_id")
        file_name = request.args.get("file_name")
        file_path = os.path.join(self.base_dir, user_id, file_name)

        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({"status": "error", "message": "Fichier non trouvé"}), 404

    def sync_status(self):
        user_id = request.args.get("user_id")
        folder_name = request.args.get("folder_name")
        folder_path = os.path.join(self.base_dir, user_id, folder_name)

        if not os.path.exists(folder_path):
            return jsonify({"status": "error", "message": "Dossier non trouvé"}), 404

        file_list = os.listdir(folder_path)
        return jsonify({"status": "success", "files": file_list})

    def create_folder(self):
        data = request.get_json()
        user_id = data.get("user_id")
        folder_name = data.get("folder_name")

        folder_path = os.path.join(self.base_dir, user_id, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        return jsonify({"status": "success", "message": f"Dossier {folder_name} créé pour {user_id}."})

    def invite_user_to_folder(self):
        data = request.get_json()
        owner_id = data.get("owner_id")
        target_user_id = data.get("target_user_id")
        folder_name = data.get("folder_name")

        source_folder = os.path.join(self.base_dir, owner_id, folder_name)
        target_folder = os.path.join(self.base_dir, target_user_id, folder_name)

        if not os.path.exists(source_folder):
            return jsonify({"status": "error", "message": "Dossier source introuvable"}), 404

        os.makedirs(target_folder, exist_ok=True)
        return jsonify({"status": "success", "message": f"{target_user_id} ajouté à {folder_name}"})


# Exemple d'exécution
if __name__ == "__main__":
    server = FileSyncAPI()
    server.start_server()
