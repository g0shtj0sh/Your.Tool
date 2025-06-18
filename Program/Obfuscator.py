from Config.Config import *
from Config.Util import *
from Config.Translates import *
import os
import base64
import marshal
import random
import string
import zlib
import itertools
import tkinter as tk
from tkinter import filedialog, messagebox, Label, Button, StringVar
from pathlib import Path
import re
import time
import subprocess
import sys

# Vérifier et installer les dépendances nécessaires
def check_and_install_dependencies():
    try:
        import tkinterdnd2
        return True
    except ImportError:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Module tkinterdnd2 non trouvé, tentative d'installation...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "tkinterdnd2"])
            print(f"\n{BEFORE + current_time_hour() + AFTER} {SUCCESS} Module tkinterdnd2 installé avec succès!")
            return True
        except Exception as e:
            print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Échec de l'installation: {str(e)}")
            return False

# Essayer d'importer tkinterdnd2, mais avoir une alternative si non disponible
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    HAS_TKDND = True
except ImportError:
    # Tenter d'installer le module
    if check_and_install_dependencies():
        try:
            from tkinterdnd2 import DND_FILES, TkinterDnD
            HAS_TKDND = True
        except ImportError:
            HAS_TKDND = False
            print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Module tkinterdnd2 non disponible, utilisation de l'interface standard.")
    else:
        HAS_TKDND = False
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Module tkinterdnd2 non disponible, utilisation de l'interface standard.")

current_language = LANGUAGE

# Définition d'une bannière pour Obfuscator
obfuscator_banner = f"""
   ██████╗ ██████╗ ███████╗██╗   ██╗███████╗ ██████╗ █████╗ ████████╗ ██████╗ ██████╗ 
  ██╔═══██╗██╔══██╗██╔════╝██║   ██║██╔════╝██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
  ██║   ██║██████╔╝█████╗  ██║   ██║███████╗██║     ███████║   ██║   ██║   ██║██████╔╝
  ██║   ██║██╔══██╗██╔══╝  ██║   ██║╚════██║██║     ██╔══██║   ██║   ██║   ██║██╔══██╗
  ╚██████╔╝██████╔╝██║     ╚██████╔╝███████║╚██████╗██║  ██║   ██║   ╚██████╔╝██║  ██║
   ╚═════╝ ╚═════╝ ╚═╝      ╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
"""

# Ne pas afficher la bannière ici pour éviter le double affichage
# Slow(obfuscator_banner)

def tr(key):
    return translations[current_language].get(key, key)

def generate_random_name(length=8):
    """Génère un nom de variable aléatoire"""
    chars = string.ascii_letters
    return ''.join(random.choice(chars) for _ in range(length))

def generate_junk_code(num_lines=5):
    """Génère du code inutile pour l'obfuscation"""
    junk_code = []
    operations = [
        "x = [i for i in range({0}, {1})]",
        "y = {{{0}: '{1}', {2}: '{3}'}}",
        "z = lambda a, b: a * b + {0}",
        "class {0}: pass",
        "def {0}(): return '{1}'",
        "try:\n        {0}\n    except:\n        pass",
        "{0} = bytes([{1}, {2}, {3}, {4}])",
        "{0} = [{1}, {2}, {3}] + [{4}, {5}, {6}]",
        "{0} = {1}.{2}({3})",
        "if {0} > {1}:\n        {2}\n    else:\n        {3}"
    ]
    
    for _ in range(num_lines):
        op = random.choice(operations)
        if "{0}" in op:
            op = op.format(
                random.randint(1, 1000),
                random.randint(1, 1000),
                random.randint(1, 1000),
                random.randint(1, 1000),
                random.randint(1, 1000),
                random.randint(1, 1000),
                random.randint(1, 1000)
            )
        junk_code.append("    " + op)
    
    return "\n".join(junk_code)

def encode_chunk(chunk):
    """Encode une portion de code en base64"""
    return base64.b64encode(chunk).decode('ascii')

def xor_encrypt(data, key):
    """Chiffre des données avec une clé en utilisant XOR"""
    return bytes(a ^ b for a, b in zip(data, itertools.cycle(key.encode())))

def basic_obfuscate(code, level=1):
    """Obfuscation basique du code"""
    # Valider le niveau d'obfuscation
    if not isinstance(level, int) or level < 1 or level > 3:
        raise ValueError("Le niveau d'obfuscation doit être un entier entre 1 et 3")
    
    # Valider le code source
    if not isinstance(code, str) or not code.strip():
        raise ValueError("Le code source est invalide ou vide")
    
    try:
        # Vérifier que le code est syntaxiquement valide
        compile(code, '<string>', 'exec')
    except SyntaxError as e:
        raise ValueError(f"Le code source contient une erreur de syntaxe : {str(e)}")
        
    if level <= 1:
        # Niveau 1: Compile et encode en base64
        code_bytes = compile(code, '<string>', 'exec')
        marshalled = marshal.dumps(code_bytes)
        encoded = encode_chunk(marshalled)
        
        obfuscated = f"""
import base64
import marshal

exec(marshal.loads(base64.b64decode('{encoded}')))
"""
    elif level == 2:
        # Niveau 2: Ajoute une couche de compression zlib
        code_bytes = compile(code, '<string>', 'exec')
        marshalled = marshal.dumps(code_bytes)
        compressed = zlib.compress(marshalled)
        encoded = encode_chunk(compressed)
        
        obfuscated = f"""
import base64
import marshal
import zlib

exec(marshal.loads(zlib.decompress(base64.b64decode('{encoded}'))))
"""
    else:
        # Niveau 3: Ajoute une couche de chiffrement XOR
        key = generate_random_name(8)
        code_bytes = compile(code, '<string>', 'exec')
        marshalled = marshal.dumps(code_bytes)
        compressed = zlib.compress(marshalled)
        encrypted = xor_encrypt(compressed, key)
        encoded = encode_chunk(encrypted)
        
        obfuscated = f"""
import base64
import marshal
import zlib
import itertools

def xor_decrypt(data, key):
    return bytes(a ^ b for a, b in zip(data, itertools.cycle(key.encode())))

exec(marshal.loads(zlib.decompress(xor_decrypt(base64.b64decode('{encoded}'), '{key}'))))
"""
    
    # Ajouter du code aléatoire pour rendre l'analyse plus difficile
    junk_header = generate_junk_code(10)
    junk_footer = generate_junk_code(10)
    
    return f"{junk_header}\n{obfuscated}\n{junk_footer}"

def advanced_obfuscate(code):
    """Obfuscation avancée du code avec plusieurs couches et techniques"""
    # Étape 1: Compile le code
    code_bytes = compile(code, '<string>', 'exec')
    marshalled = marshal.dumps(code_bytes)
    
    # Étape 2: Première couche de compression
    compressed = zlib.compress(marshalled)
    
    # Étape 3: Première clé XOR
    key1 = generate_random_name(12)
    encrypted1 = xor_encrypt(compressed, key1)
    
    # Étape 4: Deuxième couche de compression
    compressed2 = zlib.compress(encrypted1)
    
    # Étape 5: Deuxième clé XOR
    key2 = generate_random_name(12)
    encrypted2 = xor_encrypt(compressed2, key2)
    
    # Étape 6: Encodage final en base64
    encoded = encode_chunk(encrypted2)
    
    # Variables aléatoires pour rendre le décodage plus difficile à suivre
    var1 = generate_random_name(8)
    var2 = generate_random_name(8)
    var3 = generate_random_name(8)
    var4 = generate_random_name(8)
    var5 = generate_random_name(8)
    func1 = generate_random_name(8)
    func2 = generate_random_name(8)
    
    obfuscated = f"""
import base64
import marshal
import zlib
import itertools
import random
import time

{generate_junk_code(5)}

def {func1}(data, key):
    return bytes(a ^ b for a, b in zip(data, itertools.cycle(key.encode())))

{generate_junk_code(5)}

def {func2}():
    {var1} = '{encoded}'
    {var2} = base64.b64decode({var1})
    {var3} = {func1}({var2}, '{key2}')
    {var4} = zlib.decompress({var3})
    {var5} = {func1}({var4}, '{key1}')
    _x = zlib.decompress({var5})
    return marshal.loads(_x)

{generate_junk_code(5)}

exec({func2}())

{generate_junk_code(5)}
"""
    
    return obfuscated

def process_file(file_path):
    """Traite le fichier et retourne le code obfusqué"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Analyse du fichier : {reset}{file_path}{reset}")
        time.sleep(1)
        
        # Vérifier si le fichier est un script Python
        if not file_path.lower().endswith('.py'):
            print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Le fichier doit être un script Python (.py)")
            return None
        
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Début de l'obfuscation...")
        time.sleep(1)
        
        # Afficher une bannière stylisée pour les niveaux d'obfuscation
        print(f"\n{white}┌{'─' * 50}┐")
        print(f"{white}│{' ' * 15}Niveaux d'obfuscation{' ' * 15}{white}│")
        print(f"{white}└{'─' * 50}┘")
        
        print(f"{white}┌{'─' * 50}┐")
        print(f"{white}│ {reset}1{green} - Basique (compilation + base64){' ' * 12}{white}│")
        print(f"{white}│ {reset}2{green} - Intermédiaire (compression + base64){' ' * 7}{white}│")
        print(f"{white}│ {reset}3{green} - Avancé (compression + XOR + base64){' ' * 8}{white}│")
        print(f"{white}│ {reset}4{green} - Maximum (multi-couches + techniques avancées){white}│")
        print(f"{white}└{'─' * 50}┘")
        
        level = input(f"\n{INPUT} Choisissez un niveau d'obfuscation (1-4) -> {reset}")
        try:
            level = int(level)
            if level < 1 or level > 4:
                raise ValueError
        except ValueError:
            print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Niveau invalide, utilisation du niveau 1 par défaut")
            level = 1
        
        # Afficher une animation d'obfuscation
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Obfuscation en cours...")
        
        # Animation de chargement stylisée
        stages = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
        for _ in range(10):
            for stage in stages:
                sys.stdout.write(f"\r{BEFORE + current_time_hour() + AFTER} {INFO} Obfuscation en cours {stage} ")
                sys.stdout.flush()
                time.sleep(0.1)
        
        print()  # Nouvelle ligne après l'animation
        
        # Appliquer l'obfuscation selon le niveau choisi
        if level < 4:
            obfuscated_code = basic_obfuscate(code, level)
        else:
            obfuscated_code = advanced_obfuscate(code)
        
        # Créer le dossier de sortie s'il n'existe pas
        output_dir = os.path.join(tool_path, '1-Output', 'Obfuscation')
        os.makedirs(output_dir, exist_ok=True)
        
        # Créer le nom de fichier de sortie
        base_name = os.path.basename(file_path)
        output_file = os.path.join(output_dir, f"obfuscated_{base_name}")
        
        # Écrire le code obfusqué dans le fichier de sortie
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(obfuscated_code)
        
        # Afficher un résumé de l'obfuscation avec des statistiques
        original_size = len(code)
        obfuscated_size = len(obfuscated_code)
        size_increase = (obfuscated_size / original_size - 1) * 100 if original_size > 0 else 0
        
        print(f"\n{BEFORE + current_time_hour() + AFTER} {GEN_VALID} Obfuscation terminée !")
        print(f"\n{white}┌{'─' * 50}┐")
        print(f"{white}│{' ' * 16}Résumé de l'obfuscation{' ' * 16}{white}│")
        print(f"{white}├{'─' * 50}┤")
        print(f"{white}│ {green}Niveau d'obfuscation : {white}{level}{' ' * (28 - len(str(level)))}{white}│")
        print(f"{white}│ {green}Taille du fichier original : {white}{original_size} octets{' ' * (22 - len(str(original_size)))}{white}│")
        print(f"{white}│ {green}Taille du fichier obfusqué : {white}{obfuscated_size} octets{' ' * (21 - len(str(obfuscated_size)))}{white}│")
        print(f"{white}│ {green}Augmentation : {white}{size_increase:.1f}%{' ' * (34 - len(f'{size_increase:.1f}%'))}{white}│")
        print(f"{white}└{'─' * 50}┘")
        
        print(f"\n{INFO} Fichier obfusqué sauvegardé : {reset}{output_file}{reset}")
        
        return output_file
    
    except Exception as e:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Une erreur est survenue : {reset}{str(e)}{reset}")
        return None

def create_drag_drop_window():
    """Crée une fenêtre pour le glisser-déposer de fichiers"""
    if HAS_TKDND:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    
    root.title(f"Your.Tool {version_tool} - Obfuscator")
    root.geometry("600x400")
    root.resizable(False, False)
    
    # Centrer la fenêtre
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 600) // 2
    y = (screen_height - 400) // 2
    root.geometry(f"600x400+{x}+{y}")
    
    # Couleurs cohérentes avec le thème Your.Tool
    colors = {
        "white": "#ffffff",
        "green": "#00a805",  # Vert comme dans Your.Tool (au lieu du rouge)
        "dark_green": "#00a805",
        "dark_gray": "#1e1e1e",
        "gray": "#444444",
        "light_gray": "#949494",
        "background": "#262626"
    }
    
    # Essayer de charger l'icône Your.Tool
    try:
        icon_path = os.path.join(tool_path, "Img", "Your_Tool_icon.ico")
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
    except:
        pass
    
    file_path_var = StringVar()
    
    def on_drop(event):
        file_path = event.data
        
        # Nettoyer le chemin si nécessaire (pour gérer les chemins Windows avec des {})
        if file_path.startswith('{') and file_path.endswith('}'):
            file_path = file_path[1:-1]
        
        # Supprimer les guillemets si présents
        if file_path.startswith('"') and file_path.endswith('"'):
            file_path = file_path[1:-1]
        
        file_path_var.set(file_path)
        process_and_show_result(file_path)
    
    def browse_file():
        file_path = filedialog.askopenfilename(
            title="Sélectionner un script Python",
            filetypes=[("Fichiers Python", "*.py"), ("Tous les fichiers", "*.*")]
        )
        if file_path:
            file_path_var.set(file_path)
            process_and_show_result(file_path)
    
    def process_and_show_result(file_path):
        root.withdraw()  # Cacher la fenêtre pendant le traitement
        
        # Exécuter le traitement dans la console
        result_file = process_file(file_path)
        
        if result_file:
            messagebox.showinfo(
                "Obfuscation terminée",
                f"Le fichier a été obfusqué avec succès et sauvegardé dans :\n{result_file}"
            )
        else:
            messagebox.showerror(
                "Erreur",
                "Une erreur s'est produite lors de l'obfuscation. Vérifiez la console pour plus de détails."
            )
        
        root.destroy()  # Fermer la fenêtre après le traitement
    
    # Configuration du style
    root.configure(bg=colors["background"])
    
    # Bannière en haut
    banner_frame = tk.Frame(root, bg=colors["background"], height=80)
    banner_frame.pack(fill=tk.X, pady=(10, 20))
    
    banner_text = tk.Label(
        banner_frame,
        text="Your.Tool - Python Obfuscator",
        font=("Arial", 18, "bold"),
        fg=colors["green"],
        bg=colors["background"]
    )
    banner_text.pack(pady=10)
    
    version_label = tk.Label(
        banner_frame,
        text=f"Version {version_tool}",
        font=("Arial", 10),
        fg=colors["white"],
        bg=colors["background"]
    )
    version_label.pack()
    
    # Titre de l'outil
    if HAS_TKDND:
        title_text = "Déposez votre script Python ici"
    else:
        title_text = "Sélectionnez un fichier Python à obfusquer"
        
    title_label = Label(
        root, 
        text=title_text, 
        font=("Arial", 14, "bold"),
        fg=colors["white"],
        bg=colors["background"]
    )
    title_label.pack(pady=10)
    
    # Zone de drop/sélection
    drop_frame = tk.Frame(root, bg=colors["dark_gray"], width=500, height=180)
    drop_frame.pack(pady=10, padx=40, fill=tk.BOTH, expand=True)
    drop_frame.pack_propagate(False)
    
    # Icône ou image pour le glisser-déposer
    drop_icon_label = Label(
        drop_frame,
        text="📄",  # Emoji fichier
        font=("Arial", 36),
        fg=colors["green"],
        bg=colors["dark_gray"]
    )
    drop_icon_label.pack(pady=(20, 10))
    
    if HAS_TKDND:
        drop_text = "Déposez votre fichier .py ici\nou"
    else:
        drop_text = "Choisissez un fichier Python"
        
    drop_label = Label(
        drop_frame,
        text=drop_text,
        font=("Arial", 12),
        fg=colors["white"],
        bg=colors["dark_gray"]
    )
    drop_label.pack(pady=5)
    
    # Style du bouton cohérent avec Your.Tool
    browse_button = Button(
        drop_frame,
        text="Parcourir",
        font=("Arial", 10, "bold"),
        bg=colors["green"],
        fg=colors["white"],
        activebackground=colors["dark_green"],
        activeforeground=colors["white"],
        relief=tk.FLAT,
        padx=15,
        pady=5,
        command=browse_file
    )
    browse_button.pack(pady=15)
    
    # Information en bas de page
    footer_label = Label(
        root,
        text="Le fichier obfusqué sera sauvegardé dans le dossier 1-Output/Obfuscation",
        font=("Arial", 9),
        fg=colors["light_gray"],
        bg=colors["background"]
    )
    footer_label.pack(side=tk.BOTTOM, pady=10)
    
    # Configurer le drop si disponible
    if HAS_TKDND:
        drop_frame.drop_target_register(DND_FILES)
        drop_frame.dnd_bind('<<Drop>>', on_drop)
    
    root.mainloop()

def main():
    # Utiliser Title pour définir le titre de la console
    Title("Obfuscator")
    
    # Afficher la bannière avec Slow pour une animation fluide
    Slow(MainColor2(obfuscator_banner))
    
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Démarrage de l'outil d'obfuscation...")
    time.sleep(1)
    
    # Afficher un cadre stylisé pour le menu
    print(f"\n{white}┌{'─' * 50}┐")
    print(f"{white}│{' ' * 15}Mode d'utilisation{' ' * 18}{white}│")
    print(f"{white}├{'─' * 50}┤")
    print(f"{white}│ {reset}1{green} - Interface graphique{' ' * 25}{white}│")
    print(f"{white}│ {reset}2{green} - Sélection directe de fichier{' ' * 18}{white}│")
    print(f"{white}└{'─' * 50}┘")
    
    # Demander à l'utilisateur s'il souhaite utiliser l'interface graphique ou sélectionner directement un fichier
    choice = input(f"\n{INPUT} Choisissez un mode (1-2) -> {reset}")
    
    if choice == "2":
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Mode sélection directe choisi.")
        file_path = input(f"\n{INPUT} Chemin complet du fichier Python à obfusquer -> {reset}")
        
        if os.path.isfile(file_path):
            process_file(file_path)
        else:
            print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Fichier introuvable : {reset}{file_path}{reset}")
    else:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Ouverture de l'interface graphique...")
        # Créer la fenêtre
        create_drag_drop_window()
    
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Fermeture de l'outil d'obfuscation.")
    Continue()
    Reset()

if __name__ == "__main__":
    main() 