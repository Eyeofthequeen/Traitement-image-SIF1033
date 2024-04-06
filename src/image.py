import cv2
import numpy as np

from src.constantes import Couleurs


class Image:
    def __init__(self, fichier, image, nb_couleurs_max=4):
        self.fichier = fichier
        self.image = image
        self.nb_couleurs_max = nb_couleurs_max
        self.couleurs = set()

        self._identifier_couleurs_unique()

    def _convertir_rgb_vers_nom_couleur(self, rgb):
        couleurs = {
            Couleurs.BLANC: np.array([255, 255, 255]),
            Couleurs.NOIR: np.array([0, 0, 0]),
            Couleurs.ROUGE: np.array([255, 0, 0]),
            Couleurs.VERT: np.array([0, 255, 0]),
            Couleurs.BLEU: np.array([0, 0, 255]),
            Couleurs.JAUNE: np.array([255, 255, 0])
            # Ajoutez d'autres couleurs au besoin
        }

        nom_couleur_proche = None
        distance_min = float('inf')
        for nom_couleur, valeur_couleur in couleurs.items():
            distance = np.linalg.norm(rgb - valeur_couleur)
            if distance < distance_min:
                nom_couleur_proche = nom_couleur
                distance_min = distance

        return nom_couleur_proche

    def _convertir_image_vers_pixels(self, image):
        pixels = image.reshape((-1, 3))
        return np.float32(pixels)

    def _identifier_couleurs_unique(self):
        pixels = self._convertir_image_vers_pixels(self.image)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
        _, _, centers = cv2.kmeans(pixels, self.nb_couleurs_max, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        centers = np.uint8(centers) # Conversion du cluster en valeurs entières
        couleurs_uniques = centers[:, ::-1]

        for rgb in couleurs_uniques:
            self.couleurs.add(self._convertir_rgb_vers_nom_couleur(rgb))

    def redimensionner(self, largueur, hauteur=None):
        """
        Si la hauteur est None, elle sera ajustée automatiquement
        """
        dimensions = (largueur, hauteur)
        if hauteur is None:
            hauteur_originale, largeur_originale = self.image.shape[:2]
            ratio = largueur / largeur_originale
            dimensions = (largueur, int(hauteur_originale * ratio))
        return cv2.resize(self.image, dimensions)

    def convertir_niveaux_de_gris(self):
        return cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def dessiner_contours(self, titre, contours):
        tmp = self.image.copy()
        cv2.drawContours(self.image, contours, -1, (0, 255, 0), 2)
        cv2.imshow(titre, self.redimensionner(600))
        self.image = tmp
