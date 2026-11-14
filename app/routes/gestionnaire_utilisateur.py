import json
from Utilisateur import Utilisateur
import bcrypt

class GestionnaireUtilisateurs:
    def __init__(self):
        self.utilisateurs = []
        self.chemin_fichier = "utilisateur.json"
        self.chargement()

    def chargement(self):#Permet de charger les informations de l'utilisateur lorsqu'il se connecte
        with open(self.chemin_fichier, "r") as file:
            self.fichier = json.load(file)
            for user in self.fichier:#Cette boucle fait en sorte que la liste self.utilisateurs apprend les objets utilisateurs avec les attributs deja sauvegarder
                self.utilisateurs.append(Utilisateur(user["username"] ,user["password"] ,user["livres"]))

    def sauvegarde(self):#Permet de sauvegarder les attributes a la fin d'une session
        donne_json = []
        with open(self.chemin_fichier, "w") as file:
            for i in self.utilisateurs:#Cette boucle apprend les differnent attribut des utilisateurs et met chaque utilisateur dans la liste
                data = {
                    "username": i.username,
                    "password": i.password,
                    "livres_empruntes": i.livres_empruntes
            }
                donne_json.append(data)
            json.dump(donne_json, file, indent=4)

    def ajouter_utilisateur(self,user,pwd):
        existe = any(u.username == user for u in self.utilisateurs)
        if not existe:
            pwd = pwd.encode("utf-8")
            salt = bcrypt.gensalt()
            pwd_hashed = bcrypt.hashpw(pwd, salt)
            pwd_hashed = pwd_hashed.decode("utf-8")
            self.utilisateurs.append(Utilisateur(user,pwd_hashed))
            return True
        else:
            return False

    def connexion(self,username,password):
         resultat = [
            user for user in self.utilisateurs
            if username == user.username
        ]
         if resultat:
             if resultat[0].verifier_mdp(password):
                 return resultat[0]
             else:
                 return None
         else:
             return None