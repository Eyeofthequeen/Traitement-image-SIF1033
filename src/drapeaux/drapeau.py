from abc import ABC, abstractmethod

from src.image import Image
from src.commun.constantes import Difficultes


class Drapeau:
    def __init__(self, nom, couleurs, niveau: Difficultes=Difficultes.FAIBLE):
        self.nom = nom
        self.couleurs = couleurs
        self.niveau = niveau

    def couleurs_valides(self, couleurs):
        return sorted(self.couleurs) == sorted(couleurs)

    @abstractmethod
    def valider(self, image: Image):
        pass
