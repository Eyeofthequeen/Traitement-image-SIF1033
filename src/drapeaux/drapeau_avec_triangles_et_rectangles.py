import cv2
import numpy as np

from src.drapeaux.drapeau_avec_triangles import DrapeauAvecTriangles
from src.drapeaux.drapeau_avec_rectangles import DrapeauAvecRectangles
from src.image import Image
from src.commun.constantes import Difficultes

class DrapeauAvecTrianglesEtRectangles(DrapeauAvecTriangles, DrapeauAvecRectangles):
    def __init__(self, nom, couleurs, nb_rectangles=3, nb_triangles=1, vertical=True, niveau=Difficultes.FAIBLE):
        self.nb_triangles = nb_triangles
        DrapeauAvecTriangles.__init__(self, nom, couleurs, nb_triangles)
        DrapeauAvecRectangles.__init__(self, nom, couleurs, nb_rectangles, vertical, niveau)
        
    def valider(self, image: Image):
        return (self.couleurs_valides(image.couleurs)
                and self._image_contient_triangles(image)
                and self._image_contient_rectangles(image))
