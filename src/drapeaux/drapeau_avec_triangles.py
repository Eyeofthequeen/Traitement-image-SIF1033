import cv2
import numpy as np

from src.drapeaux.drapeau import Drapeau
from src.drapeaux.drapeau_avec_rectangles import DrapeauAvecRectangles
from src.image import Image
from src.commun.constantes import Difficultes

class DrapeauAvecTriangles(Drapeau):
    def __init__(self, nom, couleurs, nb_triangles=1):
        super().__init__(nom, couleurs)
        self.nb_triangles = nb_triangles

    def _image_contient_triangles(self, image):
        gris = image.convertir_niveaux_de_gris_ameliore()
        seuil_adaptatif = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 5)
        contours, _ = cv2.findContours(seuil_adaptatif, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        triangles = []
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
            if len(approx) == 3:  # Plage pour approximer un triangle
                triangles.append(approx)
                image.dessiner_contours("Contours triangles", [approx])

        nb_triangles_valide = len(triangles) == self.nb_triangles
        if nb_triangles_valide:
            image.dessiner_contours("Contours triangles", triangles)
        return nb_triangles_valide
        
    def valider(self, image: Image):
        return self.couleurs_valides(image.couleurs) and self._image_contient_triangles(image)
