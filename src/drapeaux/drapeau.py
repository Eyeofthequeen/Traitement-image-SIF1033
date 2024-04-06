from abc import ABC, abstractmethod

from src.image import Image


class Drapeau:
    def __init__(self, nom, couleurs):
        self.nom = nom
        self.couleurs = couleurs

    def couleurs_valides(self, couleurs):
        return sorted(self.couleurs) == sorted(couleurs)

    @abstractmethod
    def valider(self, image: Image):
        pass
