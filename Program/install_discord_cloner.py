# Copyright (c) Your.Tool (https://www.josh-studio.com)
# See the file 'LICENSE' for copying permission
# ----------------------------------------------------------------------------------------------------------------------------------------------------------|
# EN: 
#     - Do not touch or modify the code below. If there is an error, please contact the owner, but under no circumstances should you touch the code.
#     - Do not resell this tool, do not credit it to yours.
# FR: 
#     - Ne pas toucher ni modifier le code ci-dessous. En cas d'erreur, veuillez contacter le propriétaire, mais en aucun cas vous ne devez toucher au code.
#     - Ne revendez pas ce tool, ne le créditez pas au vôtre.

import os
import subprocess
import sys

print("\n" + "="*80)
print("NOTE: Vous n'avez normalement pas besoin d'exécuter ce script.")
print("Les dépendances pour le Discord Server Cloner sont déjà installées via Setup.bat.")
print("Ce script n'est fourni qu'en cas de problème d'installation spécifique.")
print("="*80 + "\n")

print("Installation des dépendances spécifiques pour Discord Server Cloner...")

# Liste des packages nécessaires
packages = [
    "discord.py",
    "pyperclip",
    "colorama",
    "asyncio",
    "requests"
]

# Installation des packages
for package in packages:
    print(f"Installation de {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

print("\nToutes les dépendances ont été installées avec succès!")
print("Vous pouvez maintenant utiliser l'outil Discord Server Cloner.") 