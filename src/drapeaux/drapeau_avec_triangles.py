import cv2
import numpy as np

from src.drapeaux.drapeau import Drapeau
from src.image import Image
from src.commun.constantes import Difficultes

class DrapeauAvecTriangles(Drapeau):
    def __init__(self, nom, couleurs, nb_triangles=1):
        super().__init__(nom, couleurs)
        self.nb_triangles = nb_triangles

    def _valider_angles_180(self, approx):
        nb_cotes = 3
        angles = []
        for i in range(nb_cotes):
            pt1 = approx[i][0]
            pt2 = approx[(i + 1) % nb_cotes][0]
            pt3 = approx[(i - 1) % nb_cotes][0]
            vec1 = pt1 - pt2
            vec2 = pt3 - pt2
            angle = np.arccos(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
            angles.append(np.degrees(angle))

        if 175 < sum(angles) < 185:
            # On conserve une marge d'erreur raisonnable
            return True

        return False

    def _valider_triangle_chevron(self, approx, perimetre):
        def longueur_cote_plus_long(longueurs_cotes):
            index = np.argmax(longueurs_cotes)
            return longueurs_cotes[index]

        def caracteristiques_second_cote_plus_long(longueurs_cotes, cote_plus_long):
            index = np.argmax([longueur for i, longueur in enumerate(longueurs_cotes) if i != cote_plus_long])
            return index, longueurs_cotes[index]

        longueurs_cotes = [np.linalg.norm(approx[i] - approx[(i + 1) % 4]) for i in range(4)]
        cote_plus_long = longueur_cote_plus_long(longueurs_cotes)
        index_second_cote, second_cote_plus_long = caracteristiques_second_cote_plus_long(longueurs_cotes, cote_plus_long)

        # Vérifie si deux côtés sont significativement plus longs que les deux autres côtés
        if all(longueur > cote_plus_long * 0.8 for longueur in longueurs_cotes if longueur != cote_plus_long) and \
           all(longueur > second_cote_plus_long * 0.8 for i, longueur in enumerate(longueurs_cotes) if i != index_second_cote):
            return True
        
        return False

    def _image_contient_triangles(self, image):
        gris = image.convertir_niveaux_de_gris_ameliore()
        seuil_adaptatif = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 5)
        contours, _ = cv2.findContours(seuil_adaptatif, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        triangles = []
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
            perimetre = cv2.arcLength(contour, True)
            if len(approx) == 3 and self._valider_angles_180(approx):
                triangles.append(approx)
            elif len(approx) == 4:
                perimetre = cv2.arcLength(contour, True)
                if self._valider_triangle_chevron(approx, perimetre):
                    triangles.append(approx)

        nb_triangles_valide = len(triangles) == self.nb_triangles
        if nb_triangles_valide:
            image.dessiner_contours("Contours triangles", triangles)
        return nb_triangles_valide
        
    def valider(self, image: Image):
        return self.couleurs_valides(image.couleurs) and self._image_contient_triangles(image)
