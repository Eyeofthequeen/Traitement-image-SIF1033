import cv2
import numpy as np

from src.drapeaux.drapeau_avec_trapezes import DrapeauAvecTrapezes
from src.drapeaux.drapeau_avec_rectangles import DrapeauAvecRectangles
from src.image import Image
from src.commun.constantes import Difficultes

class DrapeauAvecTrapezesEtRectangles(DrapeauAvecTrapezes, DrapeauAvecRectangles):
    def __init__(self, nom, couleurs, nb_rectangles=3, nb_trapezes=1, vertical=True, niveau=Difficultes.FAIBLE):
        DrapeauAvecTrapezes.__init__(self, nom, couleurs, nb_trapezes)
        DrapeauAvecRectangles.__init__(self, nom, couleurs, nb_rectangles, vertical, niveau=niveau)
        
    def valider(self, image: Image):
        return (self.couleurs_valides(image.couleurs)
                and self._image_contient_trapezes(image)
                and self._image_contient_rectangles(image))
