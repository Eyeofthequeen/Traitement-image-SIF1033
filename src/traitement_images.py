import cv2
import os
import numpy as np
from typing import List
from matplotlib import pyplot as plt

from src.drapeaux.etatsUnis import EtatsUnis
from src.image import Image
from src.constantes import Formes, Couleurs
from src.drapeaux.canada import Canada
from src.drapeaux.drapeau_avec_rectangles import DrapeauAvecRectangles
from src.drapeaux.drapeau_avec_cercles import DrapeauAvecCercles


Drapeaux = [
    Canada('Canada', [Couleurs.BLANC, Couleurs.ROUGE]),
    DrapeauAvecRectangles('France', [Couleurs.BLANC, Couleurs.BLEU, Couleurs.ROUGE]),
    DrapeauAvecRectangles('Russie', [Couleurs.BLANC, Couleurs.BLEU, Couleurs.ROUGE], vertical=False),
    DrapeauAvecRectangles('Espagne', [Couleurs.JAUNE, Couleurs.ROUGE], vertical=False),
    EtatsUnis('États-Unis', [Couleurs.BLANC, Couleurs.ROUGE, Couleurs.BLEU]),
    DrapeauAvecCercles('Japon', [Couleurs.BLANC, Couleurs.ROUGE]),
    DrapeauAvecCercles('Bangladesh', [Couleurs.VERT, Couleurs.ROUGE])

    #bangladesh, japon, italie, allemagne, panarabisme, suisse, vietnam, pérou
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
            self._afficher(f"Origin - {image.fichier}", image.redimensionner(600))
            print(image.fichier)
            for drapeau in Drapeaux:
                if drapeau.valider(image):
                    print(f"{drapeau.nom} - Valide")

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
