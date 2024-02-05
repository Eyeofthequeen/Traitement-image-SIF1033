import cv2
import os
import numpy as np
from matplotlib import pyplot as plt

from src.constantes import Formes


class TraitementImages:
    def __init__(self, images):
        self.images = images
        self.fenetres = []

    def _afficher(self, titre, image):
        cv2.imshow(titre, image)

    def _enregistrer(self, nom_image, image):
        cv2.imwrite(nom_image, image)

    def _afficher_images_region(self, image, contours, prefixe="roi_"): # ROI
        for i, contour in enumerate(contours):
            # Créer une image vide avec les mêmes dimensions que l'image originale
            mask = image.copy()
            mask[:] = 0

            # Dessiner le contour sur l'image vide
            cv2.drawContours(mask, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)
            contour_image = cv2.bitwise_and(image, mask) # Extraire la région
            self._afficher(f"{prefixe}{i+1}", contour_image)

    def detecter_contours_quadrilateres(self, image, carre=True, epsilon=0.04):
        image_noir_et_blanc = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresholded = cv2.adaptiveThreshold(image_noir_et_blanc, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        contours_quadrilateres = []
        for contour in contours:
            approx = cv2.approxPolyDP(contour, epsilon * cv2.arcLength(contour, True), True)

            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(contour)
                # Mesure qui représente la proportion entre la largeur et la hauteur d'un objet
                rapport_aspect = float(w) / h

                tolerence = 0.1 # Tolérance du rapport d'aspect a considérer une forme un carré
                est_carre = 1 - tolerence <= rapport_aspect <= 1 + tolerence

                if est_carre and carre:
                    contours_quadrilateres.append(contour)

                if not est_carre and not carre:
                    contours_quadrilateres.append(contour)

        return contours_quadrilateres

    def afficher_tout(self, forme: Formes):
        for image in self.images:
            self._afficher('Image originale', image)
            image_noir_et_blanc = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            contours = []
            if Formes.CARRE == forme:
                contours = self.detecter_contours_quadrilateres(image)
            elif Formes.RECTANGLE == forme:
                contours = self.detecter_contours_quadrilateres(image, carre=False)

            cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
            self._afficher('Image avec contours', image)
            self._afficher_images_region(image, contours)

            while True:
                if cv2.waitKeyEx(1) == 27: # Faire escape pour quitter
                    break

        cv2.destroyAllWindows()

    def afficher_histogramme_tout(self):
        for image in self.images:
            self._afficher('Image originale', image)

            bleu, vert, rouge = cv2.split(image)  # Division en canaux de couleur

            hist_bleu = cv2.calcHist([bleu], [0], None, [256], [0, 256])
            hist_vert = cv2.calcHist([vert], [0], None, [256], [0, 256])
            hist_rouge = cv2.calcHist([rouge], [0], None, [256], [0, 256])

            plt.plot(hist_bleu, color='blue', label='Bleu')
            plt.plot(hist_vert, color='green', label='Vert')
            plt.plot(hist_rouge, color='red', label='Rouge')

            plt.title('Histogramme couleur de l\'image')
            plt.xlabel('Intensité des pixels')
            plt.ylabel('Nombre de pixels')
            plt.legend()

            plt.savefig('histogramme.png')
            plt.close()

            hist_image = cv2.imread('histogramme.png')
            cv2.imshow('Histogramme', hist_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

