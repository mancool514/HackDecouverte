import json
import os
from app.routes.utilisateurs import Utilisateur
import bcrypt

class GestionnaireUtilisateurs:
    def __init__(self):
        self.utilisateurs = []
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.chemin_fichier = os.path.join(base_dir, "utilisateur.json")
        self.chargement()

    def chargement(self):
        if not os.path.exists(self.chemin_fichier):
            self.fichier = []
            return
        with open(self.chemin_fichier, "r", encoding="utf-8") as file:
            self.fichier = json.load(file)
            for user in self.fichier:
                self.utilisateurs.append(Utilisateur(user["username"], user["password"], user.get("livres", [])))

    def sauvegarde(self):
        donne_json = []
        with open(self.chemin_fichier, "w", encoding="utf-8") as file:
            for i in self.utilisateurs:
                data = {
                    "username": i.username,
                    "password": i.password,
                    "livres": i.livres
                }
                donne_json.append(data)
            json.dump(donne_json, file, indent=4)

    def ajouter_utilisateur(self, user, pwd):
        existe = any(u.username == user for u in self.utilisateurs)
        if not existe:
            pwd = pwd.encode("utf-8")
            salt = bcrypt.gensalt()
            pwd_hashed = bcrypt.hashpw(pwd, salt).decode("utf-8")
            self.utilisateurs.append(Utilisateur(user, pwd_hashed))
            self.sauvegarde()
            return True
        else:
            return False

    def connexion(self, username, password):
        resultat = [user for user in self.utilisateurs if username == user.username]
        if resultat:
            if resultat[0].verifier_mdp(password):
                return resultat[0]
        return None
