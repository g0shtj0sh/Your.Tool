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
import sys
import platform
import subprocess
import time

def install_requirements():
    print("Installing required modules...")
    
    # Première étape : installer les dépendances critiques
    critical_modules = [
        "setuptools",
        "wheel",
        "pefile==2022.5.30",  # Version spécifique requise par pyinstaller
    ]
    
    print("Installing critical dependencies first...")
    for module in critical_modules:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", module])
            print(f"Successfully installed {module}")
        except Exception as e:
            print(f"Failed to install {module}: {str(e)}")
    
    # Deuxième étape : installer les autres modules
    modules = [
        # Modules de base de RedTiger
        "auto-py-to-exe",
        "bcrypt",
        "beautifulsoup4",
        "browser-cookie3",
        "colorama",
        "cryptography",
        "customtkinter",
        "deep-translator",
        "discord",
        "dnspython",
        "exifread",
        "GPUtil",
        "keyboard",
        "mouse",
        "opencv-python",
        "phonenumbers",
        "piexif",
        "pillow",
        "psutil",
        "pyautogui",
        "pycryptodome",
        "pyinstaller",
        "pyqt5",
        "pyqtwebengine",
        "pywin32",
        "pyzipper",
        "rarfile",
        "requests",
        "screeninfo",
        "selenium",
        "urllib3",
        "whois",
        
        # Modules supplémentaires nécessaires
        "numpy",
        "zlib",
        "webbrowser",
        "pywin32-ctypes",
        "win32gui",
        "win32con",
        "win32api",
        "win32process",
        "win32service",
        "win32serviceutil",
        "win32security",
        "win32net",
        "win32netcon",
        "win32wnet",
        "win32event",
        "win32file",
        "win32pipe",
        "win32job",
        "win32ts",
        "win32profile",
        "win32clipboard",
        "win32console",
        "win32pdh",
        "win32pdhutil",
        "win32com",
        "Crypto",
        "PIL",
        "pytube",
        "tqdm",
        "rich",
        "discord-webhook==1.4.1"
    ]
    
    print("\nInstalling main modules...")
    
    # Désinstaller pathlib s'il est présent pour éviter les conflits
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", "pathlib"])
        print("Removed pathlib package (it's already included in Python 3)")
    except:
        pass
    
    for module in modules:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", module])
            print(f"Successfully installed {module}")
        except Exception as e:
            print(f"Failed to install {module}: {str(e)}")
            
    print("\nAll modules have been installed!")
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Installation completed! Launching Your.Tool.py...")
    time.sleep(2)
    
    # Obtenir le chemin absolu du répertoire parent (où se trouve Your.Tool.py)
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    tool_path = os.path.join(parent_dir, "Your.Tool.py")
    
    # Lancer Your.Tool.py
    try:
        subprocess.Popen([sys.executable, tool_path])
        sys.exit(0)  # Quitter le setup une fois Your.Tool.py lancé
    except Exception as e:
        print(f"Error launching Your.Tool.py: {str(e)}")
        print("Please launch Your.Tool.py manually.")
        time.sleep(5)

def main():
    # Obtenir le répertoire du script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    requirements_path = os.path.join(script_dir, "requirements.txt")
    
    if platform.system() == "Windows":
        # Windows
        try:
            print("Installing the python modules required for the Your.Tool Tool:\n")
            if os.path.exists(requirements_path):
                with open(requirements_path) as f:
                    requirements = f.read().splitlines()
                for package in requirements:
                    if package.strip():  # Ignorer les lignes vides
                        install_requirements()
                print("\nToutes les dépendances ont été installées, y compris celles pour le Discord Server Cloner!")
                print("Vous n'avez pas besoin d'exécuter install_discord_cloner.bat séparément.")
                os.system("python Your.Tool.py")
            else:
                print(f"Error: [Errno 2] No such file or directory: '{requirements_path}'")
                # Installation des modules essentiels et des dépendances du Discord Cloner
                essential_packages = [
                    "colorama", "requests", "tqdm", "beautifulsoup4", "Pillow", "numpy",
                    # Dépendances explicites du Discord Cloner
                    "discord.py", "pyperclip", "asyncio"
                ]
                print("Installing essential packages and Discord Cloner dependencies:")
                for package in essential_packages:
                    install_requirements()
                print("\nToutes les dépendances essentielles ont été installées, y compris celles pour le Discord Server Cloner!")
        except Exception as e:
            print(f"Error: {e}")
    else:
        # Linux
        try:
            print("Installing the python modules required for the Your.Tool Tool:\n")
            if os.path.exists(requirements_path):
                with open(requirements_path) as f:
                    requirements = f.read().splitlines()
                for package in requirements:
                    if package.strip():  # Ignorer les lignes vides
                        install_requirements()
                print("\nToutes les dépendances ont été installées, y compris celles pour le Discord Server Cloner!")
                print("Vous n'avez pas besoin d'exécuter install_discord_cloner.bat séparément.")
                os.system("python3 Your.Tool.py")
            else:
                print(f"Error: [Errno 2] No such file or directory: '{requirements_path}'")
                # Installation des modules essentiels et des dépendances du Discord Cloner
                essential_packages = [
                    "colorama", "requests", "tqdm", "beautifulsoup4", "Pillow", "numpy",
                    # Dépendances explicites du Discord Cloner
                    "discord.py", "pyperclip", "asyncio"
                ]
                print("Installing essential packages and Discord Cloner dependencies:")
                for package in essential_packages:
                    install_requirements()
                print("\nToutes les dépendances essentielles ont été installées, y compris celles pour le Discord Server Cloner!")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
