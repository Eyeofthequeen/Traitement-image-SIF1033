# Manuel d'utilisateur - Script de traitement d'images
Notre équipe de trois personnes travaillera sur le développement d'un programme visant à détecter les drapeaux de différents pays. Les drapeaux présentent une diversité de formes géométriques, de couleurs, et parfois des symboles uniques ou similaires. Cette combinaison en fait un choix idéal pour le traitement d'images. L'objectif principal sera de fournir au programme des images de drapeaux permettant ainsi au système de deviner à quel pays chaque drapeau appartient en appliquant divers traitements.

Pour la première phase de ce projet, nous commencerons par la détection de quadrilatères.

## Membres de l'équipe
Jérémy Veillette <br>
Dylan Sicard-Smith <br>
Miriam Davydov

## Description
Le script offre une interface en ligne de commande qui lit des photos et affiche l'image original ainsi que les images objets (régions ROI ou contours) présents dans les images.

## Utilisation
```bash
python3 script.py [-h] [-c CHEMIN]
```

*Note: utilisez la commande python de votre terminal.*

## Options

### `-h`, `--help`

Affiche cette aide.

### `-c CHEMIN`, `--chemin CHEMIN`

Chemin vers la photo ou le dossier d'images. Cette option est utilisée pour spécifier le chemin des images à traiter.

## Notes
Le script affiche les images dans des fenêtres graphiques, veillez faire ESC sur ces fenêtres pour traiter la prochaine image ou CTRL+C dans le terminal pour terminer le traitement.
