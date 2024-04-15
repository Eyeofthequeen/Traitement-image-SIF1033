import cv2
import numpy as np

from typing import List, Tuple

from src.image import Image
from src.commun.constantes import Difficultes
from src.commun.outils import verifier_avec_marge_erreur

class ValidateurFormesImage:
    @staticmethod
    def valider_triangles(image: Image, nb_triangles):
        def _valider_angles_180(approx):
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

            if 178 < sum(angles) < 182:
                # On conserve une marge d'erreur raisonnable
                return True

            return False

        def _valider_triangle_chevron(approx, perimetre):
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

        gris = image.convertir_niveaux_de_gris_ameliore()
        seuil_adaptatif = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 5)
        contours, _ = cv2.findContours(seuil_adaptatif, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        triangles = []
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
            perimetre = cv2.arcLength(contour, True)
            if len(approx) == 3 and _valider_angles_180(approx):
                triangles.append(approx)
            elif len(approx) == 4:
                perimetre = cv2.arcLength(contour, True)
                if _valider_triangle_chevron(approx, perimetre):
                    triangles.append(approx)

        nb_triangles_valide = len(triangles) == nb_triangles
        if nb_triangles_valide:
            image.dessiner_contours("Contours triangles", triangles)

        return nb_triangles_valide
 
    @staticmethod
    def valider_cercles(image: Image, nb_cercles):
        gris = image.convertir_niveaux_de_gris()
        contours = cv2.Canny(gris, 30, 100)
        cercles = cv2.HoughCircles(contours, cv2.HOUGH_GRADIENT, 2, image.image.shape[0]/2)

        cercles_valides = cercles is not None and len(cercles[0]) == nb_cercles
        if cercles_valides:
            image.dessiner_contours_cercles(f'Cercles pour {image.fichier}', cercles[0])

        return cercles_valides

    @staticmethod
    def valider_etoiles(image: Image, nb_etoiles):
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

        return verifier_avec_marge_erreur(len(etoiles), nb_etoiles, 1)

    @staticmethod
    def valider_trapezes(image: Image, nb_trapezes):
        def _valider_trapeze(approx):
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = w / float(h)

            if 0.5 <= aspect_ratio <= 2:
                if cv2.isContourConvex(approx):  # Un trapèze c'est convexe
                    return True
            return False 

        gris = image.convertir_niveaux_de_gris_ameliore()
        seuil = cv2.adaptiveThreshold(gris, 256, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        contours, _ = cv2.findContours(seuil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        trapezoids = []
        for contour in contours:
            epsilon = 0.03 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            if len(approx) == 4 and _valider_trapeze(approx):
                trapezoids.append(approx)

        nb_trapezes_valide = len(trapezoids) == nb_trapezes
        if nb_trapezes_valide:
            image.dessiner_contours(f'Contours trapeze {image.fichier}', trapezoids)
        return nb_trapezes_valide

    @staticmethod
    def valider_rectangles(image: Image, niveau, nb_rectangles, vertical):
        niveau_elevee = niveau == Difficultes.ELEVEE
        if niveau_elevee:
            gris = image.convertir_niveaux_de_gris_agressif()
        else:
            gris = image.convertir_niveaux_de_gris_ameliore()

        seuil = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        contours, _ = cv2.findContours(seuil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

        rectangles = []
        for contour in contours:
            perimetre = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.01 * perimetre, True)
            # Un rectangle a 4 côtés.
            # Par ailleurs, des fois, un rectangle peut avoir 5 côtés en conservant les propriétés d'un rectangle.
            if len(approx) == 4 or (len(approx) == 5 and niveau_elevee):
                x, y, w, h = cv2.boundingRect(contour)
                rect_vertical = h > w and vertical
                rect_horizontal = w > h and not vertical
                
                if rect_vertical or rect_horizontal:
                    rectangles.append(approx)

        nb_rectangles_valide = len(rectangles) == nb_rectangles
        if nb_rectangles_valide:
            image.dessiner_contours(
                f"Contours des rectangles {'verticaux' if vertical else 'horizontaux'} pour {image.fichier}", rectangles
            )

        return nb_rectangles_valide

