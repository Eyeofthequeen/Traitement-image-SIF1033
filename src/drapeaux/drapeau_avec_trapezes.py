import cv2
import numpy as np

from src.drapeaux.drapeau import Drapeau
from src.image import Image

class DrapeauAvecTrapezes(Drapeau):
    def __init__(self, nom, couleurs, nb_trapezes=1):
        super().__init__(nom, couleurs)
        self.nb_trapezes = nb_trapezes

    def _valider_trapeze(self, approx):
        x, y, w, h = cv2.boundingRect(approx)
        aspect_ratio = w / float(h)

        if 0.5 <= aspect_ratio <= 2:
            if cv2.isContourConvex(approx):  # Un trapèze c'est convexe
                return True

        return False 

    def _image_contient_trapezes(self, image):
        gris = image.convertir_niveaux_de_gris_ameliore()
        seuil = cv2.adaptiveThreshold(gris, 256, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        contours, _ = cv2.findContours(seuil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        trapezoids = []
        for contour in contours:
            epsilon = 0.03 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            if len(approx) == 4 and self._valider_trapeze(approx):
                trapezoids.append(approx)

        nb_trapezes_valide = len(trapezoids) == self.nb_trapezes
        if nb_trapezes_valide:
            image.dessiner_contours(f'Contours trapeze {image.fichier}', trapezoids)
        return nb_trapezes_valide

    def valider(self, image: Image):
        return self.couleurs_valides(image.couleurs) and self._image_contient_trapezes(image)
