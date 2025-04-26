# SynchronisationSystem
Synchronisation System DROPBOX Type
# Système de Synchronisation de Fichiers - IFT585 (TP3-TP4)

## Description
Ce projet implémente un système de synchronisation de fichiers inspiré de Dropbox, Google Drive et OneDrive.  
Il permet à plusieurs clients de :
- Se connecter via UDP (authentification rapide et fiable).
- Synchroniser leurs fichiers avec un serveur central (protocole REST).
- Télécharger, téléverser et partager des répertoires entre utilisateurs.

Le projet a été développé en Python dans le cadre du cours **IFT585 - Télématique** à l'Université de Sherbrooke.

---

## Fonctionnalités principales
- Authentification des utilisateurs via UDP.
- Téléversement et téléchargement de fichiers via REST.
- Synchronisation des répertoires utilisateurs.
- Création de dossiers distants.
- Invitation d'utilisateurs pour le partage de dossiers.

---

## Prérequis
Assurez-vous d'avoir installé :
- **Python 3.10** ou supérieur
- **Flask** (`pip install flask`)
- **requests** (`pip install requests`)
- **Werkzeug** (`pip install werkzeug`)

---

## Procédure d’exécution du système 
1. Demarrage du systeme 
cd Server
python rest_server.py

2. Lancer le serveur d'authentification UDP
cd Authentication
python auth_server.py

3. Lancer le client pour tester le système complet
python full_system_test.py

---

## Fonctionnalités testées automatiquement
- Le script full_system_test.py effectue :

- Authentification de l’utilisateur via UDP.

- Création d’un dossier distant sur le serveur.

- Téléversement (upload) d’un fichier test.

- Synchronisation (récupération de la liste des fichiers).

- Téléchargement du fichier uploadé.

- Invitation d’un autre utilisateur à collaborer sur un dossier.

- Toutes les étapes sont affichées dans le terminal avec des messages de confirmation.

---

## Ce qui fonctionne dans le projet
* Authentification UDP fiable avec gestion de la connexion utilisateur.

* Synchronisation REST entre le client et le serveur.

* Création dynamique de répertoires pour chaque utilisateur.

* Téléversement sécurisé de fichiers.

* Téléchargement correct des fichiers sauvegardés.

* Invitation d'autres utilisateurs à accéder à un dossier partagé.

* Architecture modulaire et propre (modules Authentication, Server, Client, Storage, Models).


---

## Installation
Clonez le projet sur votre machine :

```bash
git clone [https://depot.dinf.usherbrooke.ca/dinf/cours/h25/ift585/projet2/EQ09/tp4-systeme-de-synchronisation/-/tree/dev?ref_type=heads]
cd system-sync-tp4

---

