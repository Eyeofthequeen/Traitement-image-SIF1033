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
        contours = cv2.Canny(gris, 30, 100)
        cercles = cv2.HoughCircles(contours, cv2.HOUGH_GRADIENT, 2, image.image.shape[0]/2)

        cercles_valides = cercles is not None and len(cercles[0]) == self.nb_cercles
        if cercles_valides:
            image.dessiner_contours_cercles(f'Cercles pour {image.fichier}', cercles[0])

        return cercles_valides

    def valider(self, image: Image):
        return self.couleurs_valides(image.couleurs) and self._image_contient_cercles(image)
