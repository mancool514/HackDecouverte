import bcrypt

from app.routes.livre import Livre


class Utilisateur:
    def __init__(self, username, password, livres=None):
        self.username = username
        self.password = password  # hash bcrypt
        self.livres = livres or []

    def ajouter_livre(self, livre):
        if livre not in self.livres:
            self.livres.append(livre)
            return True
        return False

    def retirer_livre(self, livre):
        if livre in self.livres:
            self.livres.remove(livre)
            return True
        return False

    def trouver_livre(self, livre_id):
        return next((l for l in self.livres if l.id == livre_id), None)

    def verifier_mdp(self, mdp):
        hash_bytes = self.password.encode("utf-8") if isinstance(self.password, str) else self.password
        return bcrypt.checkpw(mdp.encode("utf-8"), hash_bytes)

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "livres": [l.to_dict() for l in self.livres],
        }

    @classmethod
    def from_dict(cls, data):
        livres = [Livre.from_dict(l) for l in data.get("livres", [])]
        return cls(data["username"], data["password"], livres)
