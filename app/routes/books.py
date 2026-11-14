class Livre:
    def __init__(self,titre, auteur,pages,pageslu = None):
        self.titre = titre
        self.auteur = auteur
        self.pages = pages
        self.pagesLu = pageslu if pageslu is not None else 0




