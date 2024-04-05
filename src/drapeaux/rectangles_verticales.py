from src.drapeaux.drapeau import Drapeau

class RectanglesVerticales(Drapeau):
    def __init__(self, nom, couleurs, nb_rectangles=3):
        super().__init__(nom, couleurs)
        self.nb_rectangles = nb_rectangles

    def _image_contient_rectangles(self):
        pass