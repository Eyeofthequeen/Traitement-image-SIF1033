import cv2
import os
import numpy as np
from typing import List
from matplotlib import pyplot as plt

from src.image import Image
from src.commun.constantes import Formes, Couleurs, Difficultes
from src.drapeaux import *

TroisRectangles = (Formes.RECTANGLE, 3)
UnCercle = (Formes.CERCLE, 1)
UnTriangle = (Formes.TRIANGLE, 1)

Drapeaux = [
    Liban('Liban', [Couleurs.VERT, Couleurs.ROUGE, Couleurs.BLANC]),
    Canada('Canada', [Couleurs.BLANC, Couleurs.ROUGE]),
    DrapeauAvecFormes(
        'Bahamas', [Couleurs.JAUNE, Couleurs.BLEU, Couleurs.NOIR], [UnTriangle, TroisRectangles], vertical=False, niveau=Difficultes.ELEVEE
    ),
    DrapeauAvecFormes('Guyana', [Couleurs.NOIR, Couleurs.ROUGE, Couleurs.JAUNE, Couleurs.BLANC, Couleurs.VERT], [(Formes.TRIANGLE, 5)]),
    DrapeauAvecFormes('Coree du Nord', [Couleurs.ROUGE, Couleurs.BLEU, Couleurs.BLANC], [UnCercle, (Formes.ETOILE, 1)]),
    DrapeauAvecFormes('Jamaique', [Couleurs.NOIR, Couleurs.JAUNE, Couleurs.VERT], [(Formes.TRIANGLE, 4)]),
    DrapeauAvecFormes('France', [Couleurs.BLANC, Couleurs.BLEU, Couleurs.ROUGE], [TroisRectangles]),
    DrapeauAvecFormes('Russie', [Couleurs.BLANC, Couleurs.BLEU, Couleurs.ROUGE], [TroisRectangles], vertical=False),
    DrapeauAvecFormes('Espagne', [Couleurs.JAUNE, Couleurs.ROUGE], [TroisRectangles], vertical=False),
    DrapeauAvecFormes('États-Unis', [Couleurs.BLANC, Couleurs.ROUGE, Couleurs.BLEU], [(Formes.ETOILE, 50)]),
    DrapeauAvecFormes('Vietnam', [Couleurs.ROUGE, Couleurs.JAUNE], [(Formes.ETOILE, 1)]),
    DrapeauAvecFormes('Japon', [Couleurs.BLANC, Couleurs.ROUGE], [UnCercle]),
    DrapeauAvecFormes('Chine', [Couleurs.ROUGE, Couleurs.JAUNE], [(Formes.ETOILE, 5)]),
    DrapeauAvecFormes('Bangladesh', [Couleurs.VERT, Couleurs.ROUGE], [UnCercle]),
    DrapeauAvecFormes('Italie', [Couleurs.VERT, Couleurs.ROUGE, Couleurs.BLANC], [TroisRectangles]),
    DrapeauAvecFormes('Allemagne', [Couleurs.NOIR, Couleurs.ROUGE, Couleurs.JAUNE], [TroisRectangles], vertical=False), 
    DrapeauAvecFormes('Pérou', [Couleurs.BLANC, Couleurs.ROUGE], [TroisRectangles]), 
    DrapeauAvecFormes(
        'Kuwait', [Couleurs.VERT, Couleurs.NOIR, Couleurs.BLANC, Couleurs.ROUGE], [(Formes.TRAPEZE, 1), TroisRectangles], vertical=False, niveau=Difficultes.ELEVEE
    ),
    # DrapeauAvecFormes(
        # 'Panarabisme', [Couleurs.BLANC, Couleurs.ROUGE, Couleurs.NOIR, Couleurs.VERT], [UnTriangle, TroisRectangles], vertical=False, niveau=Difficultes.ELEVEE
    # ),
    DrapeauAvecFormes(
        'Soudan', [Couleurs.BLANC, Couleurs.ROUGE, Couleurs.NOIR, Couleurs.VERT], [UnTriangle, TroisRectangles], vertical=False, niveau=Difficultes.ELEVEE
    ), # Panarabisme doit être commenté pour que celui-ci soit détecté parce qu'ils sont identiques. On ne valide pas l'ordre des couleurs.
    DrapeauAvecFormes('Tchéquie', [Couleurs.BLANC, Couleurs.ROUGE, Couleurs.BLEU], [UnTriangle, (Formes.RECTANGLE, 2)], vertical=False),
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
