import cv2
import numpy as np

from src.drapeaux.drapeau import Drapeau
from src.image import Image

class Liban(Drapeau):
    def __init__(self, nom, couleurs):
        super().__init__(nom, couleurs)
        self.nb_sapins = 1
        self.proportion_vert = 90

    def _valider_sapin_vert(self, image, sapins):
        for contour in sapins:
            x, y, w, h = cv2.boundingRect(contour)
            region_vert = image[y:y+h, x:x+w] # Region de l'image correspondant au contour

            gris = cv2.cvtColor(region_vert, cv2.COLOR_BGR2GRAY)
            seuil_vert_region = cv2.threshold(gris, 100, 255, cv2.THRESH_BINARY)[1] # Seuil du vert
            proportion_vert = np.count_nonzero(seuil_vert_region) / (w * h)

            return proportion_vert * 100 > self.proportion_vert
        return False

    def _valider_sapins(self, image, sapins):
        nb_sapins_valide = len(sapins) == self.nb_sapins

        if not nb_sapins_valide:
            return nb_sapins_valide

        image.dessiner_contours('Contour sapin', sapins)
        return self._valider_sapin_vert(image.image, sapins)

    def _extraire_sapins(self, image):
        seuil_min = 10000
        gris = image.convertir_niveaux_de_gris()
        seuil_adaptatif = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        contours, _ = cv2.findContours(seuil_adaptatif, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        sapins = []
        for contour in contours:
            if cv2.contourArea(contour) > seuil_min:
                sapins.append(contour)
        return sapins

    def valider(self, image: Image):
        sapins = self._extraire_sapins(image)
        return self.couleurs_valides(image.couleurs) and self._valider_sapins(image, sapins)
