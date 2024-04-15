import cv2
import os
import numpy as np
from typing import List
from matplotlib import pyplot as plt

from src.image import Image
from src.commun.constantes import Formes, Couleurs, Difficultes
from src.drapeaux import *


Drapeaux = [
    Liban('Liban', [Couleurs.VERT, Couleurs.ROUGE, Couleurs.BLANC]),
    Canada('Canada', [Couleurs.BLANC, Couleurs.ROUGE]),
    DrapeauAvecTrianglesEtRectangles(
        'Bahamas', [Couleurs.JAUNE, Couleurs.BLEU, Couleurs.NOIR], vertical=False, niveau=Difficultes.ELEVEE
    ),
    DrapeauAvecTriangles('Guyana', [Couleurs.NOIR, Couleurs.ROUGE, Couleurs.JAUNE, Couleurs.BLANC, Couleurs.VERT], 5),
    DrapeauAvecCerclesEtEtoiles('Coree du Nord', [Couleurs.ROUGE, Couleurs.BLEU, Couleurs.BLANC]),
    DrapeauAvecTriangles('Jamaique', [Couleurs.NOIR, Couleurs.JAUNE, Couleurs.VERT], 4),
    DrapeauAvecRectangles('France', [Couleurs.BLANC, Couleurs.BLEU, Couleurs.ROUGE]),
    DrapeauAvecRectangles('Russie', [Couleurs.BLANC, Couleurs.BLEU, Couleurs.ROUGE], vertical=False),
    DrapeauAvecRectangles('Espagne', [Couleurs.JAUNE, Couleurs.ROUGE], vertical=False),
    DrapeauAvecEtoiles('États-Unis', [Couleurs.BLANC, Couleurs.ROUGE, Couleurs.BLEU], nb_etoiles=50),
    DrapeauAvecEtoiles('Vietnam', [Couleurs.ROUGE, Couleurs.JAUNE]),
    DrapeauAvecCercles('Japon', [Couleurs.BLANC, Couleurs.ROUGE]),
    DrapeauAvecEtoiles('Chine', [Couleurs.ROUGE, Couleurs.JAUNE], nb_etoiles=5),
    DrapeauAvecCercles('Bangladesh', [Couleurs.VERT, Couleurs.ROUGE]),
    DrapeauAvecRectangles('Italie', [Couleurs.VERT, Couleurs.ROUGE, Couleurs.BLANC]),
    DrapeauAvecRectangles('Allemagne', [Couleurs.NOIR, Couleurs.ROUGE, Couleurs.JAUNE], vertical=False),
    DrapeauAvecRectangles('Pérou', [Couleurs.BLANC, Couleurs.ROUGE]),
    DrapeauAvecTrapezesEtRectangles('Kuwait', [Couleurs.VERT, Couleurs.NOIR, Couleurs.BLANC, Couleurs.ROUGE], vertical=False, niveau=Difficultes.ELEVEE),
    # DrapeauAvecTrianglesEtRectangles(
        # 'Panarabisme', [Couleurs.BLANC, Couleurs.ROUGE, Couleurs.NOIR, Couleurs.VERT], vertical=False, niveau=Difficultes.ELEVEE
    # ),
    DrapeauAvecTrianglesEtRectangles(
        'Soudan', [Couleurs.BLANC, Couleurs.ROUGE, Couleurs.NOIR, Couleurs.VERT], vertical=False, niveau=Difficultes.ELEVEE
    ), # Panarabisme doit être commenté pour que celui-ci soit détecté parce qu'ils sont identiques. On ne valide pas l'ordre des couleurs.
    DrapeauAvecTrianglesEtRectangles(
        'Tchéquie', [Couleurs.BLANC, Couleurs.ROUGE, Couleurs.BLEU], nb_rectangles=2, nb_triangles=1, vertical=False
    ),
    #suisse
]


class TraitementImages:
    def __init__(self, images: List[Image]):
        self.images = images
        self.fenetres = []

    def _afficher(self, titre, image):
        cv2.imshow(titre, image)

    def _enregistrer(self, nom_image, image):
        cv2.imwrite(nom_image, image)

    def detecter_drapeaux_de_chaque_image(self):
        for image in self.images:
            self._afficher(f"Origin - {image.fichier}", image.image)
            print(image.fichier)
            for drapeau in Drapeaux:
                if drapeau.valider(image):
                    print(f"{drapeau.nom} - Valide")
                    break

            while True:
                if cv2.waitKeyEx(1) == 27:  # Faire escape pour quitter ou pour passer à l'image suivante
                    cv2.destroyAllWindows()
                    break
