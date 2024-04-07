import cv2
import numpy as np

from src.drapeaux.drapeau import Drapeau
from src.image import Image
from src.commun import image_outils
from src.commun.constantes import Couleurs

class Liban(Drapeau):
    def __init__(self, nom, couleurs):
        super().__init__(nom, couleurs)
        self.nb_sapins = 1
        # Quand la région sera extraite, elle prendra plus que juste le sapin donc,
        # la proportion de vert considéré valide peut être largement inférieur a 100%.
        self.proportion_vert = 40

    def _valider_sapin_vert(self, image: Image, sapins):
        for sapin in sapins:
            region_sapin = image.extraire_region(sapin)

            nb_pixels_verts = image_outils.extraire_nb_pixels_pour_couleur(Couleurs.VERT, region_sapin)
            h, w = region_sapin.shape[:2]
            nb_pixels_total = h * w
            proportion_vert = (nb_pixels_verts / nb_pixels_total) * 100

            return proportion_vert > self.proportion_vert
        return False

    def _valider_sapins(self, image, sapins):
        nb_sapins_valide = len(sapins) == self.nb_sapins

        if not nb_sapins_valide:
            return nb_sapins_valide

        image.dessiner_contours('Contour sapin', sapins)
        return self._valider_sapin_vert(image, sapins)

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
