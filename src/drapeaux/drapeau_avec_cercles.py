import cv2
import numpy as np

from src.drapeaux.drapeau import Drapeau
from src.image import Image


class DrapeauAvecCercles(Drapeau):
    def __init__(self, nom, couleurs, nb_cercles=1):
        super().__init__(nom, couleurs)
        self.nb_cercles = nb_cercles

    def _image_contient_cercles(self, image: Image):
        gris = image.convertir_niveaux_de_gris()
        gris = cv2.medianBlur(gris, 5)
        cercles = cv2.HoughCircles(gris, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=0, maxRadius=0)
        return cercles is not None and len(cercles[0]) >= self.nb_cercles

    def valider(self, image: Image):
        return self.couleurs_valides(image.couleurs) and self._image_contient_cercles(image)
