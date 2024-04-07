import cv2
import numpy as np

from src.drapeaux.drapeau import Drapeau
from src.image import Image
from src.commun.outils import verifier_avec_marge_erreur


class DrapeauAvecEtoiles(Drapeau):
    def __init__(self, nom, couleurs, nb_etoiles=1, marge_erreur=1):
        super().__init__(nom, couleurs)
        self.nb_etoiles = nb_etoiles
        self.marge_erreur = marge_erreur

    def _image_contient_etoile(self, image):
        gris = image.convertir_niveaux_de_gris()

        seuil_adaptatif = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        contours, _ = cv2.findContours(seuil_adaptatif, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) 

        etoiles = []
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
            if len(approx) == 10:  # 10 côté égal une étoile
                etoiles.append(approx)
        if len(etoiles) > 0:
            image.dessiner_contours(
                f"Contours des etoiles pour {image.fichier}", etoiles
            )

        return verifier_avec_marge_erreur(len(etoiles), self.nb_etoiles, self.marge_erreur)

    def valider(self, image: Image):
        return self.couleurs_valides(image.couleurs) and self._image_contient_etoile(image)
