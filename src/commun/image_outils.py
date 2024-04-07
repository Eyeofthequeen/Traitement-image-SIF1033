import cv2
import numpy as np

from .constantes import Couleurs

def extraire_nb_pixels_pour_couleur(couleur, image):
    if Couleurs.VERT == couleur:
        plage_couleur_basse = np.array([0, 100, 0], dtype=np.uint8)
        plage_couleur_haute = np.array([100, 255, 100], dtype=np.uint8)
    elif Couleurs.ROUGE == couleur:
        plage_couleur_basse = np.array([150, 0, 0], dtype=np.uint8)
        plage_couleur_haute = np.array([255, 100, 100], dtype=np.uint8)
    elif Couleurs.BLEU == couleur:
        plage_couleur_basse = np.array([0, 0, 100], dtype=np.uint8)
        plage_couleur_haute = np.array([100, 100, 255], dtype=np.uint8)

    masque = cv2.inRange(image, plage_couleur_basse, plage_couleur_haute)
    return np.count_nonzero(masque)
