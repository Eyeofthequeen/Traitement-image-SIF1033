import cv2
from src.drapeaux.drapeau import Drapeau
from src.drapeaux.drapeau_avec_rectangles import DrapeauAvecRectangles
from src.image import Image


class Canada(DrapeauAvecRectangles):
    def __init__(self, nom, couleurs):
        super().__init__(nom, couleurs, nb_rectangles=2)
        self.nb_erables = 1

    def _image_contient_erables(self, image):
        gris = image.convertir_niveaux_de_gris()

        seuil_adaptatif = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        contours, _ = cv2.findContours(seuil_adaptatif, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        erables = []
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
            if 18 <= len(approx) <= 24:  # Plage pour approximer une feuille d'érable
                erables.append(approx)
                image.dessiner_contours("Contours feuilles erables", [approx])

        return len(erables) == self.nb_erables

    def valider(self, image: Image):
        return (self.couleurs_valides(image.couleurs)
                and self._image_contient_rectangles(image)
                and self._image_contient_erables(image))
