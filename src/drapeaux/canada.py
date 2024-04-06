import cv2
from src.drapeaux.drapeau import Drapeau
from src.image import Image


class Canada(Drapeau):
    def __init__(self, nom, couleurs, erable=1):
        super().__init__(nom, couleurs)
        self.erable=erable

    def _image_contient_erable(self, image):
        gris = image.convertir_niveaux_de_gris()

        seuil_adaptatif = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        contours, _ = cv2.findContours(seuil_adaptatif, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        erables = []
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)
            if len(approx) == 21:  # 21 côté égal la feuille d'érable sans la tige
                erables.append(approx)
        if len(erables) > 0:
            image.dessiner_contours(
                f"Contours des feuilles d'érable", erables
            )
        if len(erables)!=1: #il ne doit y avoir qu'une seule feuille
            return False
        return len(erables) == self.erable

    def valider(self, image: Image):
        return self.couleurs_valides(image.couleurs) and self._image_contient_erable(image)
