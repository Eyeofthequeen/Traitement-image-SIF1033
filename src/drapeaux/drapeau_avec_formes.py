import cv2
import numpy as np

from typing import List, Tuple

from src.drapeaux.drapeau import Drapeau
from src.image import Image
from src.commun.constantes import Difficultes, Formes
from src.validateur_formes_image import ValidateurFormesImage

class DrapeauAvecFormes(Drapeau):
    def __init__(self, nom, couleurs, formes: List[Tuple[Formes, int]], vertical=True, niveau: Difficultes=Difficultes.FAIBLE):
        super().__init__(nom, couleurs, niveau)
        self.vertical = vertical
        self.formes = formes

    def valider(self, image: Image):
        est_valide = self.couleurs_valides(image.couleurs)

        for forme in self.formes:
            if not est_valide:
                break

            type_forme = forme[0]
            nb_formes = forme[1]

            if type_forme == Formes.RECTANGLE:
                est_valide = ValidateurFormesImage.valider_rectangles(image, self.niveau, nb_formes, self.vertical)
            elif type_forme == Formes.TRAPEZE:
                est_valide = ValidateurFormesImage.valider_trapezes(image, nb_formes)
            elif type_forme == Formes.CARRE:
                pass
            elif type_forme == Formes.CERCLE:
                est_valide = ValidateurFormesImage.valider_cercles(image, nb_formes)
            elif type_forme == Formes.ETOILE:
                est_valide = ValidateurFormesImage.valider_etoiles(image, nb_formes)
            elif type_forme == Formes.TRIANGLE:
                est_valide = ValidateurFormesImage.valider_triangles(image, nb_formes)
            else:
                raise Exception(f"La forme {forme[0]} n'est pas prise en charge.")

        return est_valide
