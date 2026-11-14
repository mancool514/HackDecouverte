import math
import uuid
from datetime import date


class Livre:
    def __init__(self, titre, auteur, pages_totales, date_limite,
                 pages_initiales=0, lectures=None, id=None):
        self.id = id or uuid.uuid4().hex[:8]
        self.titre = titre
        self.auteur = auteur
        self.pages_totales = int(pages_totales)
        self.date_limite = date_limite          # chaîne "AAAA-MM-JJ"
        self.pages_initiales = int(pages_initiales or 0)  # où l'utilisateur était rendu à l'ajout
        self.lectures = lectures or []           # [{"date": "AAAA-MM-JJ", "pages": 10}, ...]

    # --- Lectures -----------------------------------------------------------
    def lire(self, pages, jour):
        """Ajoute une séance de lecture (ex: 10 pages le 2026-11-03)."""
        self.lectures.append({"date": jour, "pages": int(pages)})
        self.lectures.sort(key=lambda l: l["date"])

    def retirer_lecture(self, index):
        if 0 <= index < len(self.lectures):
            self.lectures.pop(index)
            return True
        return False

    # --- Statistiques -------------------------------------------------------
    @property
    def pages_lues(self):
        total = self.pages_initiales + sum(l["pages"] for l in self.lectures)
        return min(total, self.pages_totales)

    @property
    def pages_restantes(self):
        return self.pages_totales - self.pages_lues

    @property
    def pourcentage(self):
        if self.pages_totales <= 0:
            return 0
        return round(self.pages_lues * 100 / self.pages_totales)

    @property
    def est_termine(self):
        return self.pages_restantes <= 0

    @property
    def jours_restants(self):
        """Nombre de jours de lecture restants, aujourd'hui inclus."""
        return (date.fromisoformat(self.date_limite) - date.today()).days + 1

    @property
    def en_retard(self):
        return not self.est_termine and self.jours_restants <= 0

    @property
    def pages_par_jour(self):
        if self.est_termine:
            return 0
        if self.jours_restants <= 0:
            return self.pages_restantes
        return math.ceil(self.pages_restantes / self.jours_restants)

    # --- Sérialisation JSON -------------------------------------------------
    def to_dict(self):
        return {
            "id": self.id,
            "titre": self.titre,
            "auteur": self.auteur,
            "pages_totales": self.pages_totales,
            "date_limite": self.date_limite,
            "pages_initiales": self.pages_initiales,
            "lectures": self.lectures,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            titre=data["titre"],
            auteur=data["auteur"],
            pages_totales=data["pages_totales"],
            date_limite=data["date_limite"],
            pages_initiales=data.get("pages_initiales", 0),
            lectures=data.get("lectures", []),
            id=data.get("id"),
        )
