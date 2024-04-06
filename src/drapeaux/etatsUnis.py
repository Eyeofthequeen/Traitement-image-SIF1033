import cv2
from src.drapeaux.drapeau import Drapeau
from src.image import Image


class EtatsUnis(Drapeau):
    def __init__(self, nom, couleurs, etoile=50):
        super().__init__(nom, couleurs)
        self.etoile=etoile

    def _image_contient_etoile(self, image):
        gris = image.convertir_niveaux_de_gris()

        seuil_adaptatif = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        contours, _ = cv2.findContours(seuil_adaptatif, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        etoiles = []
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.02* cv2.arcLength(contour, True), True)
            if len(approx) == 10:  # 10 côté égal une étoile
                etoiles.append(approx)
        if len(etoiles) > 0:
            image.dessiner_contours(
                f"Contours des étoiles", etoiles
            )
        return len(etoiles) == self.etoile

    def valider(self, image: Image):
        return self.couleurs_valides(image.couleurs) and self._image_contient_etoile(image)
