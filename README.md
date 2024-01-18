# Manuel d'utilisateur - Script de traitement d'images

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
