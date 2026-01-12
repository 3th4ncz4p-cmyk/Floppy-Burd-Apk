[app]

# (str) Titre de ton application
title = Floppy Burd

# (str) Nom du package (sans espaces ni caractères spéciaux)
package.name = floppyburd

# (str) Domaine du package (ex: org.caveman)
package.domain = org.cavemanstudios

# (str) Répertoire où se trouve le main.py ( . signifie racine)
source.dir = .

# (list) Extensions de fichiers à inclure
# IMPORTANT : on ajoute wav et json pour tes sons et ta sauvegarde
source.include_exts = py,png,jpg,wav,json

# (list) Liste des dépendances (Python et modules)
requirements = python3,pygame

# (str) Version de ton application
version = 1.0

# (str) Orientation (portrait est mieux pour un Flappy Bird)
orientation = portrait

# (bool) Utiliser l'écran complet
fullscreen = 1

# (list) Permissions Android (Vibrations ou écriture si besoin)
# android.permissions = VIBRATE, WRITE_EXTERNAL_STORAGE

# (int) API Android cible (33 ou 34 est recommandé pour 2024)
android.api = 33

# (int) API Android minimum (21 = Android 5.0)
android.minapi = 21

# (str) Nom de l'icône
icon.filename = icon_burd.png

# (str) Image de splash (chargement)
# presplash.filename = %(source.dir)s/Caveman_Studios.png

# (bool) Indique si l'application est en mode debug
android.debug_artifacts = 0

[buildozer]

# (int) Niveau de log (2 pour voir les erreurs détaillées)
log_level = 2

# (str) Répertoire de build de buildozer
build_dir = ./.buildozer

# (str) Répertoire de sortie des APK (bin)
bin_dir = ./bin
