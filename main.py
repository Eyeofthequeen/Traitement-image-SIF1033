import cv2
import os
import argparse

from src.outils import extraire_images, extraire_image, est_image
from src.traitement_images import TraitementImages
from src.constantes import Formes


def main():
    # Déclaration des arguments pour la ligne de commande
    parser = argparse.ArgumentParser(description='Traitement d\'images avec affichage de fenêtres.', add_help=False)
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Affiche cette aide.')
    parser.add_argument('chemin', help='Chemin vers la photo ou le dossier d\'images.')
    args = parser.parse_args()

    if os.path.isdir(args.chemin):
        images = extraire_images(args.chemin)
    elif os.path.isfile(args.chemin) and est_image(args.chemin):
        images = [extraire_image(args.chemin)]

    traitement = TraitementImages(images)
    traitement.afficher_tout(Formes.CARRE)


if __name__ == "__main__":
    main()
