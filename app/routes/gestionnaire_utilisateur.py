import json
from pathlib import Path

from app.routes.utilisateurs import Utilisateur

# Base de données fixe (2 utilisateurs de démo) : app/data/utilisateurs.json
CHEMIN_FICHIER = Path(__file__).resolve().parent.parent / "data" / "utilisateurs.json"


class GestionnaireUtilisateurs:
    def __init__(self, chemin_fichier=CHEMIN_FICHIER):
        self.chemin_fichier = Path(chemin_fichier)
        self.utilisateurs = []
        self.chargement()

    def chargement(self):
        """Charge les utilisateurs (et leurs livres) depuis le fichier JSON."""
        with open(self.chemin_fichier, "r", encoding="utf-8") as file:
            donnees = json.load(file)
        self.utilisateurs = [Utilisateur.from_dict(u) for u in donnees]

    def sauvegarde(self):
        """Écrit l'état actuel (livres, lectures) dans le fichier JSON."""
        with open(self.chemin_fichier, "w", encoding="utf-8") as file:
            json.dump([u.to_dict() for u in self.utilisateurs], file, indent=4, ensure_ascii=False)

    def trouver(self, username):
        return next((u for u in self.utilisateurs if u.username == username), None)

    def connexion(self, username, password):
        user = self.trouver(username)
        if user and user.verifier_mdp(password):
            return user
        return None
