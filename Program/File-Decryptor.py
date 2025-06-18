from Config.Util import *
from Config.Config import *
from Config.Translates import *

current_language = LANGUAGE

def tr(key):
    return translations[current_language].get(key, key)

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import padding
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    import os
    import base64
except Exception as e:
    ErrorModule(e)

Title(f"File Decryptior")

def validate_encrypted_file(file_path):
    """Valide le fichier à déchiffrer"""
    if not os.path.exists(file_path):
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} File does not exist")
        return False
        
    if not os.path.isfile(file_path):
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Not a valid file")
        return False
        
    # Vérifier si le fichier est bien un fichier chiffré
    if not file_path.endswith('.enc'):
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} File is not encrypted")
        return False
        
    # Vérifier si le fichier n'est pas vide
    if os.path.getsize(file_path) == 0:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} File is empty")
        return False
        
    # Vérifier si le fichier a la taille minimale requise (sel + iv + contenu)
    if os.path.getsize(file_path) < 48:  # 16 (sel) + 16 (iv) + 16 (bloc minimum)
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} File is corrupted")
        return False
        
    return True

def decrypt_file(encrypted_file_content, password):
    try:
        # Vérifier les entrées
        if not encrypted_file_content or len(encrypted_file_content) < 32:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid encrypted file content")
            return None
            
        if not password:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Password cannot be empty")
            return None
            
        salt = encrypted_file_content[:16]
        iv = encrypted_file_content[16:32]
        encrypted_content = encrypted_file_content[32:]
        
        try:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            key = kdf.derive(password.encode())
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            padded_data = decryptor.update(encrypted_content) + decryptor.finalize()
            unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
            data = unpadder.update(padded_data) + unpadder.finalize()
            return data
        except ValueError as ve:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid padding or corrupted data")
            return None
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} {tr('WrongPassword')}")
            return None
    except Exception as e:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Unexpected error: {str(e)}")
        return None

try:
    Slow(f"""{encrypted_banner}
{secondary}[{primary}01{secondary}] {primary}->{secondary} Decrypt File
    """)

    choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Choice -> {reset}")

    if choice not in ['1', '01']:
        ErrorChoice()

    file_path = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Path to decrypt -> {secondary}")
    
    if not validate_encrypted_file(file_path):
        Continue()
        Reset()
        
    password = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Password for decryption -> {secondary}")
    
    if not password:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Password cannot be empty")
        Continue()
        Reset()

    try:
        with open(file_path, 'rb') as file:
            encrypted_file_content = file.read()
    except Exception as e:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error reading file: {e}")
        raise e

    try:
        decrypted_content = decrypt_file(encrypted_file_content, password)
        if decrypted_content is None:
            Continue()
            Reset()
            
        output_directory = "1-Output/FileDecrypted"
        os.makedirs(output_directory, exist_ok=True)
        file_name = os.path.basename(file_path)
        decrypted_file_path = os.path.join(output_directory, file_name.replace('.enc', ''))
        
        with open(decrypted_file_path, 'wb') as file:
            file.write(decrypted_content)
        
        print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Decrypted content saved to: {decrypted_file_path}{reset}")
    except Exception as e:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error during decryption: {e}")

    Continue()
    Reset()
except Exception as e:
    Error(e)

