import cv2
import numpy as np

from src.drapeaux.drapeau import Drapeau
from src.image import Image

class DrapeauAvecRectangles(Drapeau):
    def __init__(self, nom, couleurs, nb_rectangles=3, vertical=True):
        super().__init__(nom, couleurs)
        self.nb_rectangles = nb_rectangles
        self.vertical = vertical

    def _image_contient_rectangles(self, image):
        gris = image.convertir_niveaux_de_gris()

        seuil_adaptatif = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        contours, _ = cv2.findContours(seuil_adaptatif, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        rectangles = []
        for contour in contours:
            perimetre = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimetre, True)
            if len(approx) == 4:  # 4 côtés donc rectangle
                x, y, w, h = cv2.boundingRect(contour)
                rect_vertical = h > w and self.vertical
                rect_horizontal = w > h and not self.vertical
                
                if rect_vertical or rect_horizontal:
                    rectangles.append(approx)

        nb_rectangles_valide = len(rectangles) == self.nb_rectangles
        if nb_rectangles_valide:
            image.dessiner_contours(
                f"Contours des rectangles {'verticaux' if self.vertical else 'horizontaux'} pour {image.fichier}", rectangles
            )

        return nb_rectangles_valide
        
    def valider(self, image: Image):
        return self.couleurs_valides(image.couleurs) and self._image_contient_rectangles(image)
