class Livre:
    def __init__(self,titre, auteur,pages_totales,date_limite,pageslu = None):
        self.titre = titre
        self.auteur = auteur
        self.pages_totales = pages_totales
        self.pagesLu = pageslu if pageslu is not None else 0
        self.pagesRestante = pages_totales-pageslu
        self.date_limite = date_limite

    def lire(self,lu):
        self.pagesLu += lu

    def wallah_pardon(self, pas_lu):
        self.pagesLu -= pas_lu






