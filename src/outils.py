import cv2
import os

def extraire_images(chemin_dossier):
    images = []
    fichiers = [f for f in os.listdir(chemin_dossier) if os.path.isfile(os.path.join(chemin_dossier, f))]

    for fichier in fichiers:
        chemin = os.path.join(chemin_dossier, fichier)

        if est_image(fichier):
            images.append(cv2.imread(chemin))
    return images

def extraire_image(chemin_image):
    return cv2.imread(chemin_image, cv2.IMREAD_COLOR)

def est_image(fichier):
    return fichier.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
