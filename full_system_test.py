# full_system_test.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Client')))
from client_app import ClientApp

if __name__ == "__main__":
    client = ClientApp("user1", "pass1")

    print("\n==== ÉTAPE 1 : Authentification UDP ====")
    client.authenticate_udp()

    print("\n==== ÉTAPE 2 : Création d'un dossier distant ====")
    client.create_folder("dossier_test")

    print("\n==== ÉTAPE 3 : Téléversement d'un fichier ====")
    client.upload("testfile.pdf")  # IMPORTANT : testfile.pdf MUST BE IN THE SAME DIRECTORY AS THIS SCRIPT

    print("\n==== ÉTAPE 4 : Synchronisation du dossier ====")
    client.sync_rest()

    print("\n==== ÉTAPE 5 : Téléchargement du fichier ====")
    client.download("testfile.pdf")

    print("\n==== ÉTAPE 6 : Invitation d'un autre utilisateur ====")
    client.invite_user("user2", "dossier_test")

    print("\n====  TEST TERMINÉ AVEC SUCCÈS  ====\n")
