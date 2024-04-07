import cv2

from src.image import Image
from src.drapeaux.drapeau_avec_cercles import DrapeauAvecCercles
from src.drapeaux.drapeau_avec_etoiles import DrapeauAvecEtoiles

class DrapeauAvecCerclesEtEtoiles(DrapeauAvecCercles, DrapeauAvecEtoiles):
    def __init__(self, nom, couleurs, nb_etoiles=1, nb_cercles=1, marge_erreur=1):
        DrapeauAvecCercles.__init__(self, nom, couleurs, nb_cercles)
        DrapeauAvecEtoiles.__init__(self, nom, couleurs, nb_etoiles, marge_erreur)

    def valider(self, image: Image):
        return (self.couleurs_valides(image.couleurs)
                and self._image_contient_cercles(image)
                and self._image_contient_etoile(image))

