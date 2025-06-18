# Copyright (c) Your.Tool (https://www.josh-studio.com)
# See the file 'LICENSE' for copying permission
# ----------------------------------------------------------------------------------------------------------------------------------------------------------|
# EN: 
#     - Do not touch or modify the code below. If there is an error, please contact the owner, but under no circumstances should you touch the code.
#     - Do not resell this tool, do not credit it to yours.
# FR: 
#     - Ne pas toucher ni modifier le code ci-dessous. En cas d'erreur, veuillez contacter le propriétaire, mais en aucun cas vous ne devez toucher au code.
#     - Ne revendez pas ce tool, ne le créditez pas au vôtre.

from Config.Util import *
from Config.Config import *
try:
    import os
    import subprocess
    import ctypes
    import sys
except Exception as e:
    ErrorModule(e)

Title("Rat Discord (Premium)")

try:
    exe_path = os.path.join(tool_path, "Your.Tool-Rat-Builder.exe")
    
    if os.path.exists(exe_path):
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Démarrage du constructeur de RAT Discord...")
        
        if os_name == "Windows":
            # Vérifier si le script a des droits d'administrateur
            def is_admin():
                try:
                    return ctypes.windll.shell32.IsUserAnAdmin()
                except:
                    return False
            
            if is_admin():
                # Si déjà admin, lancer directement
                subprocess.Popen(exe_path)
            else:
                try:
                    # Essayer de lancer avec runas pour obtenir des privilèges élevés
                    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Élévation des privilèges nécessaire...")
                    ctypes.windll.shell32.ShellExecuteW(None, "runas", exe_path, None, None, 1)
                except Exception as e:
                    print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Erreur lors de l'élévation des privilèges: {str(e)}")
                    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Essai de méthode alternative...")
                    
                    # Méthode alternative avec création d'un fichier batch temporaire
                    bat_path = os.path.join(tool_path, "temp_admin_launch.bat")
                    with open(bat_path, "w") as bat_file:
                        bat_file.write(f'@echo off\n')
                        bat_file.write(f'echo Lancement du RAT Builder avec privilèges administrateur...\n')
                        bat_file.write(f'powershell -Command "Start-Process -FilePath \'{exe_path}\' -Verb RunAs"\n')
                        bat_file.write(f'del "%~f0"\n')  # Auto-suppression du fichier batch
                    
                    # Exécution du fichier batch
                    os.startfile(bat_path)
        else:
            print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Cette fonctionnalité est uniquement disponible sur Windows.")
            
        input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press to continue -> " + reset)
        Reset()
    else:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Le fichier {exe_path} est introuvable.")
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Assurez-vous que le fichier 'Your.Tool-Rat-Builder.exe' est dans le répertoire principal.")
        input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press to continue -> " + reset)
        Reset()
except Exception as e:
    Error(e)
