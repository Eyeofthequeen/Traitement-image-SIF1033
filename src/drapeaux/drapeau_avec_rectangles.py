import cv2
import numpy as np

from src.drapeaux.drapeau import Drapeau
from src.image import Image
from src.commun.constantes import Difficultes

class DrapeauAvecRectangles(Drapeau):
    def __init__(self, nom, couleurs, nb_rectangles=3, vertical=True, niveau: Difficultes=Difficultes.FAIBLE):
        super().__init__(nom, couleurs)
        self.nb_rectangles = nb_rectangles
        self.vertical = vertical
        self.niveau = niveau

    def _image_contient_rectangles(self, image):
        niveau_elevee = self.niveau == Difficultes.ELEVEE
        if niveau_elevee:
            gris = image.convertir_niveaux_de_gris_agressif()
        else:
            gris = image.convertir_niveaux_de_gris_ameliore()

        seuil = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        contours, _ = cv2.findContours(seuil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

        rectangles = []
        for contour in contours:
            perimetre = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.01 * perimetre, True)
            # Un rectangle a 4 côtés.
            # Par ailleurs, des fois, un rectangle peut avoir 5 côtés en conservant les propriétés d'un rectangle.
            if len(approx) == 4 or (len(approx) == 5 and niveau_elevee):
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
