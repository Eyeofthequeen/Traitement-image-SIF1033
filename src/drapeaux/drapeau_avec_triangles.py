import cv2
import numpy as np

from src.drapeaux.drapeau_avec_rectangles import DrapeauAvecRectangles
from src.image import Image

class DrapeauAvecTriangles(DrapeauAvecRectangles):
    def __init__(self, nom, couleurs, nb_rectangles, nb_triangles=1, vertical=True):
        super().__init__(nom, couleurs, nb_rectangles=nb_rectangles)
        self.nb_triangles = nb_triangles
        self.vertical = vertical

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
        print("nb triangles", len(triangles))
        return len(triangles) == self.nb_triangles
        
    def valider(self, image: Image):
        print(image.couleurs)
        return self.couleurs_valides(image.couleurs) and self._image_contient_triangles(image) and self._image_contient_rectangles(image)
