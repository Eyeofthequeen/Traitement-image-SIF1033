from src.drapeaux.drapeau import Drapeau
from src.image import Image


class Canada(Drapeau):
    def __init__(self, nom, couleurs):
        super().__init__(nom, couleurs)

    def valider(self, image: Image):
        return self.couleurs_valides(image.couleurs)
