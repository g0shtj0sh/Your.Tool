#!/usr/bin/env python3
import os
import pyzipper
import shutil

# Chemin des fichiers et dossiers
tool_path = os.path.dirname(os.path.abspath(__file__))
source_file = os.path.join(tool_path, "Program", "FileDetectedByAntivirus", "VirusBuilderOptions.py")
output_zip = os.path.join(tool_path, "Program", "FileDetectedByAntivirus", "Password(yourtool).zip")

# Création du ZIP avec mot de passe
def create_password_protected_zip():
    print(f"Création du fichier ZIP protégé par mot de passe: {output_zip}")
    with pyzipper.AESZipFile(output_zip, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zf:
        zf.pwd = b'yourtool'
        zf.write(source_file, os.path.basename(source_file))
    print(f"Fichier ZIP créé avec succès")

if __name__ == "__main__":
    create_password_protected_zip() 