import cv2
import numpy as np

from src.commun.constantes import Couleurs


class Image:
    def __init__(self, fichier, image, nb_couleurs_max=5):
        self.fichier = fichier
        self.image = image
        self.nb_couleurs_max = nb_couleurs_max
        self.couleurs = set()

        self.image = self.redimensionner(800)
        self._identifier_couleurs_unique()

    def _convertir_rgb_vers_nom_couleur(self, rgb):
        # Définition des plages de couleur pour chaque couleur
        couleurs = {
            Couleurs.BLANC: ([200, 200, 200], [255, 255, 255]),
            Couleurs.NOIR: ([0, 0, 0], [50, 50, 50]),
            Couleurs.ROUGE: ([150, 0, 0], [255, 100, 100]),
            Couleurs.VERT: ([0, 100, 0], [100, 255, 110]),
            Couleurs.BLEU: ([0, 0, 100], [100, 125, 255]),
            Couleurs.JAUNE: ([200, 175, 0], [255, 255, 100]),
        }

        # Vérification de l'appartenance à une plage de couleur
        for couleur, (min_vals, max_vals) in couleurs.items():
            if np.all(rgb >= min_vals) and np.all(rgb <= max_vals):
                return couleur

        # Si aucune couleur ne correspond, retourner None ou une couleur par défaut
        return None

    def _convertir_image_vers_pixels(self, image):
        pixels = image.reshape((-1, 3))
        return np.float32(pixels)

    def _identifier_couleurs_unique(self):
        pixels = self._convertir_image_vers_pixels(self.image)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
        _, _, centers = cv2.kmeans(pixels, self.nb_couleurs_max, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        centers = np.uint8(centers) # Conversion du cluster en valeurs entières
        couleurs_uniques = centers[:, ::-1]

        for rgb in couleurs_uniques:
            nom_couleur = self._convertir_rgb_vers_nom_couleur(rgb)
            if nom_couleur:
                self.couleurs.add(nom_couleur)

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
        cv2.imshow(titre, self.image)
        self.image = tmp

    def extraire_region(self, contour):
        x, y, w, h = cv2.boundingRect(contour)
        return self.image[y:y+h, x:x+w]

    def convertir_niveaux_de_gris_ameliore(self):
        gris = self.convertir_niveaux_de_gris()
        normalized_img = cv2.normalize(gris, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        sharpened_img = cv2.filter2D(normalized_img, -1, np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]))
        return cv2.equalizeHist(sharpened_img)

    def convertir_niveaux_de_gris_agressif(self):
        gris = self.convertir_niveaux_de_gris()
        normalized_img = cv2.normalize(gris, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        sharpened_img = cv2.filter2D(normalized_img, -1, np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]))
        equalized = cv2.equalizeHist(sharpened_img)

        laplacian = cv2.Laplacian(equalized, cv2.CV_64F)

        ajuste = cv2.convertScaleAbs(laplacian, alpha=1.2, beta=50)
        return ajuste

    def seuillage_aggressif(self):
        kernel = np.ones((3, 3), np.uint8)
        gris = self.convertir_niveaux_de_gris_ameliore()
        seuil = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        gris = cv2.dilate(seuil, kernel, iterations=100)
        return seuil
