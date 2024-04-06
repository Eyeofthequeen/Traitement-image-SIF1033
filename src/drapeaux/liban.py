import cv2

from src.drapeaux.drapeau import Drapeau
from src.image import Image

class Liban(Drapeau):
    def __init__(self, nom, couleurs):
        super().__init__(nom, couleurs)

    def _image_contient_sapin(self, image: Image):
        seuil_min = 10000
        gris = image.convertir_niveaux_de_gris()
        seuil_adaptatif = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        # Trouver les contours dans le masque binaire
        contours, _ = cv2.findContours(seuil_adaptatif, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        sapins = []
        for contour in contours:
            if cv2.contourArea(contour) > seuil_min:
                sapins.append(contour)

        image.dessiner_contours('Contour sapin', sapins)

        return len(sapins) > 0


    def valider(self, image: Image):
        return self.couleurs_valides(image.couleurs) and self._image_contient_sapin(image)
