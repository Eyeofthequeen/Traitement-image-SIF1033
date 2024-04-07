import cv2
import os
import argparse

from src.traitement_images import TraitementImages
from src.commun.constantes import Formes
from src.commun.outils import extraire_images, extraire_image, est_image


def main():
    # Déclaration des arguments pour la ligne de commande
    parser = argparse.ArgumentParser(description='Traitement d\'images avec affichage de fenêtres.', add_help=False)
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Affiche cette aide.')
    parser.add_argument('chemin', help='Chemin vers la photo ou le dossier d\'images.')
    parser.add_argument('-histo', '--histogramme', action='store_true', help="Affiche l'histogramme de l'image.")
    parser.add_argument('-e', '--edges', help='Affiche les contours des images.')
    args = parser.parse_args()

    if os.path.isdir(args.chemin):
        images = extraire_images(args.chemin)
    elif os.path.isfile(args.chemin) and est_image(args.chemin):
        images = [extraire_image(args.chemin)]

    traitement = TraitementImages(images)
    # traitement.afficher_tout(Formes.CARRE)

    traitement.detecter_drapeaux_de_chaque_image()


    if args.histogramme:
        traitement.afficher_histogramme_tout()


if __name__ == "__main__":
    main()
