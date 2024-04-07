import cv2
import os
import numpy as np
from typing import List
from matplotlib import pyplot as plt

from src.drapeaux.drapeau_avec_triangles_et_rectangles import DrapeauAvecTrianglesEtRectangles
from src.image import Image
from src.commun.constantes import Formes, Couleurs, Difficultes
from src.drapeaux.canada import Canada
from src.drapeaux.liban import Liban
from src.drapeaux.drapeau_avec_rectangles import DrapeauAvecRectangles
from src.drapeaux.drapeau_avec_cercles import DrapeauAvecCercles
from src.drapeaux.drapeau_avec_etoiles import DrapeauAvecEtoiles
from src.drapeaux.drapeau_avec_etoiles_et_cercle import DrapeauAvecCerclesEtEtoiles


Drapeaux = [
    Liban('Liban', [Couleurs.VERT, Couleurs.ROUGE, Couleurs.BLANC]),
    Canada('Canada', [Couleurs.BLANC, Couleurs.ROUGE]),
    DrapeauAvecCerclesEtEtoiles('Coree du Nord', [Couleurs.ROUGE, Couleurs.BLEU, Couleurs.BLANC]),
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
    DrapeauAvecTrianglesEtRectangles(
        'Panarabisme', [Couleurs.BLANC, Couleurs.ROUGE, Couleurs.NOIR, Couleurs.VERT], nb_rectangles=3, nb_triangles=1, vertical=False, niveau=Difficultes.ELEVEE
    ),
    DrapeauAvecTrianglesEtRectangles(
        'Tchéquie', [Couleurs.BLANC, Couleurs.ROUGE, Couleurs.BLEU], nb_rectangles=2, nb_triangles=1, vertical=False
    ),
    #panarabisme, suisse
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
                    break

    # def afficher_histogramme_tout(self):
        # for image in self.images:
            # self._afficher('Image originale', image)

            # bleu, vert, rouge = cv2.split(image)  # Division en canaux de couleur

            # hist_bleu = cv2.calcHist([bleu], [0], None, [256], [0, 256])
            # hist_vert = cv2.calcHist([vert], [0], None, [256], [0, 256])
            # hist_rouge = cv2.calcHist([rouge], [0], None, [256], [0, 256])

            # plt.plot(hist_bleu, color='blue', label='Bleu')
            # plt.plot(hist_vert, color='green', label='Vert')
            # plt.plot(hist_rouge, color='red', label='Rouge')

            # plt.title('Histogramme couleur de l\'image')
            # plt.xlabel('Intensité des pixels')
            # plt.ylabel('Nombre de pixels')
            # plt.legend()

            # plt.savefig('histogramme.png')
            # plt.close()

            # hist_image = cv2.imread('histogramme.png')
            # cv2.imshow('Histogramme', hist_image)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
