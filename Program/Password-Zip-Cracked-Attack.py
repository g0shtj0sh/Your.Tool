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
    import rarfile
    import pyzipper
    import string
    import tkinter
    from tkinter import filedialog
    from concurrent.futures import ThreadPoolExecutor
    import zipfile
    import time
    import os
except Exception as e:
    ErrorModule(e)

Title(f"Password Zip Cracked Attack")

try:
    def ChooseZipRarFile():
        try:
            print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Select a .zip or .rar file in the dialog box that will open...")
            file = ""
            if sys.platform.startswith("win"):
                # Créer et configurer la fenêtre Tkinter
                root = tkinter.Tk()
                root.title(f"{name_tool} {version_tool} - Select a file")
                root.geometry("1x1+0+0")  # Petite fenêtre pour ne pas perturber l'utilisateur
                try:
                    root.iconbitmap(os.path.join(tool_path, "Img", "Your_Tool_icon.ico"))
                except:
                    pass
                root.attributes('-topmost', True)  # Garder la fenêtre au premier plan
                
                # Donne un peu de temps pour que la fenêtre soit initialisée
                root.update()
                time.sleep(0.5)
                
                # Ouvrir la boîte de dialogue de sélection de fichier
                file = filedialog.askopenfilename(
                    parent=root,
                    title=f"{name_tool} {version_tool} - Choose .zip or .rar file", 
                    filetypes=[("ZIP/RAR files", "*.zip;*.rar"), ("ZIP files", "*.zip"), ("RAR files", "*.rar")]
                )
                
                # Fermer la fenêtre Tkinter
                root.destroy()
            else:
                # Pour Linux
                root = tkinter.Tk()
                root.withdraw()
                file = filedialog.askopenfilename(
                    title=f"{name_tool} {version_tool} - Choose .zip or .rar file", 
                    filetypes=[("ZIP/RAR files", "*.zip;*.rar"), ("ZIP files", "*.zip"), ("RAR files", "*.rar")]
                )
                root.destroy()
            
            # Vérifier si un fichier a été sélectionné
            if file:
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} File selected: {white + file}")
                return file
            else:
                # Si aucun fichier n'a été sélectionné, demander manuellement
                print(f"{BEFORE + current_time_hour() + AFTER} {WARNING} No file selected in dialog. Please enter path manually.")
                return input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Enter the path to the .zip or .rar file -> {reset}")
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error with file selection: {str(e)}")
            return input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Enter the path to the .zip or .rar file -> {reset}")

    def CountEncryptedFiles(file):
        count = 0
        try:
            if file.lower().endswith('.zip'):
                try:
                    with pyzipper.AESZipFile(file) as archive:
                        for filename in archive.namelist():
                            try:
                                archive.extract(filename, path="1-Output/TempExtract", pwd=b'wrongpassword')  
                            except RuntimeError: 
                                count += 1
                except:
                    print(f"{BEFORE + current_time_hour() + AFTER} {WARNING} Could not open ZIP file with pyzipper, trying standard zipfile...")
                    with zipfile.ZipFile(file) as archive:
                        for filename in archive.namelist():
                            try:
                                archive.extract(filename, path="1-Output/TempExtract", pwd=b'wrongpassword')  
                            except RuntimeError: 
                                count += 1
            elif file.lower().endswith('.rar'):
                with rarfile.RarFile(file) as archive:
                    for filename in archive.namelist():
                        try:
                            archive.extract(filename, path="1-Output/TempExtract", pwd='wrongpassword')  
                        except Exception:  # Remplacer rarfile.BadPassword par Exception générique
                            count += 1
            return count
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error counting encrypted files: {str(e)}")
            return count
        
    def CheckPassword(file, password_test):
        global password_found
        try:
            if file.lower().endswith('.zip'):
                try:
                    with pyzipper.AESZipFile(file) as archive:
                        for filename in archive.namelist():
                            try:
                                archive.extract(filename, path="1-Output/Extracted", pwd=password_test.encode())
                                password_found += 1
                                print(f'{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} File: {white + filename} {green}Password: {white + password_test + reset}')
                            except:
                                pass
                except:
                    with zipfile.ZipFile(file) as archive:
                        for filename in archive.namelist():
                            try:
                                archive.extract(filename, path="1-Output/Extracted", pwd=password_test.encode())
                                password_found += 1
                                print(f'{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} File: {white + filename} {green}Password: {white + password_test + reset}')
                            except:
                                pass
            elif file.lower().endswith('.rar'):
                with rarfile.RarFile(file) as archive:
                    for filename in archive.namelist():
                        try:
                            # Pour les fichiers RAR, utiliser bytes au lieu de string
                            if isinstance(password_test, str):
                                pwd_bytes = password_test.encode()
                            else:
                                pwd_bytes = password_test
                            archive.extract(filename, path="1-Output/Extracted", pwd=pwd_bytes)
                            password_found += 1
                            print(f'{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} File: {white + filename} {green}Password: {white + password_test + reset}')
                        except:
                            pass
            return password_found > 0
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error checking password: {str(e)}")
            return False

    def RandomCharacter(count):
        global generated_passwords, password_found
        try:
            threads_number = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Threads Number -> {reset}"))
            characters_number_min = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Password Characters Number Min -> {reset}"))
            characters_number_max = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Password Characters Number Max -> {reset}"))
        except:
            ErrorNumber()

        generated_passwords = set()
        password_found = 0
        all_characters = string.ascii_letters + string.digits + string.punctuation

        def GeneratePassword():
            return ''.join(random.choice(all_characters) for _ in range(random.randint(characters_number_min, characters_number_max)))

        def TestCracked():
            global generated_passwords, password_found
            while password_found < count:
                password_test = GeneratePassword()
                if password_test not in generated_passwords:
                    generated_passwords.add(password_test)
                    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Testing password: {white}{password_test}")
                    if CheckPassword(file, password_test):
                        if password_found == count:
                            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} All files successfully cracked! Files extracted to 1-Output/Extracted")
                            Continue()
                            Reset()

        def Request():
            with ThreadPoolExecutor(max_workers=threads_number) as executor:
                executor.map(lambda _: TestCracked(), range(threads_number))

        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Brute force password cracking in progress.. (It can be long){reset}")
        
        # Créer le dossier d'extraction s'il n'existe pas
        os.makedirs("1-Output/Extracted", exist_ok=True)
        
        try:
            while password_found < count:
                Request()
        except KeyboardInterrupt:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Password cracking interrupted by user.")

    def WorldList():
        global password_found
        path_folder_worldlist = os.path.join(tool_path, "2-Input", "WorldList")
        
        # Vérifier si le dossier existe
        if not os.path.exists(path_folder_worldlist):
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} WorldList folder not found: {white + path_folder_worldlist}")
            os.makedirs(path_folder_worldlist, exist_ok=True)
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Created WorldList folder. Please add password lists there.")
            Continue()
            Reset()
            return
        
        # Obtenir la liste des fichiers dans le dossier
        all_files = os.listdir(path_folder_worldlist)
        
        # Filtrer les fichiers selon leur extension
        wordlist_files = []
        compressed_files = []
        
        for f in all_files:
            file_path = os.path.join(path_folder_worldlist, f)
            if os.path.isfile(file_path):
                if f.lower().endswith(('.txt', '.lst', '.dict')):
                    wordlist_files.append(f)
                elif f.lower().endswith(('.zip', '.rar')):
                    compressed_files.append(f)
        
        # Avertir l'utilisateur si des fichiers compressés sont trouvés
        if compressed_files and not wordlist_files:
            print(f"{BEFORE + current_time_hour() + AFTER} {WARNING} Found compressed files in WorldList folder, but no text wordlists:")
            for cf in compressed_files:
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} {white}{cf}{red} (needs to be extracted)")
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Please extract these files to use them as wordlists.")
            Continue()
            Reset()
            return
        
        # Vérifier s'il y a des wordlists disponibles
        if not wordlist_files:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} No wordlist files found in: {white + path_folder_worldlist}")
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Add .txt, .lst, or .dict files to this directory.")
            Continue()
            Reset()
            return
        
        # Afficher les wordlists disponibles
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Found {white}{len(wordlist_files)}{red} wordlist files:")
        for idx, wf in enumerate(wordlist_files):
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} {white}{idx+1}.{red} {white}{wf}")
        
        password_found = 0
        
        # Créer le dossier d'extraction s'il n'existe pas
        os.makedirs("1-Output/Extracted", exist_ok=True)
        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Password cracking by wordlist in progress... (This may take a long time){reset}")

        # Parcourir chaque fichier wordlist
        for file_list in wordlist_files:
            try:
                with open(os.path.join(path_folder_worldlist, file_list), 'r', encoding='utf-8', errors='ignore') as f:
                    passwords_tested = 0
                    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Testing passwords from: {white}{file_list}")
                    
                    for line in f:
                        passwords_tested += 1
                        password = line.strip()
                        
                        # Afficher un message de progression toutes les 1000 tentatives
                        if passwords_tested % 1000 == 0:
                            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Progress: {white}{passwords_tested}{red} passwords tested from {white}{file_list}")
                        
                        if CheckPassword(file, password):
                            if password_found == count:
                                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} All files successfully cracked! Files extracted to 1-Output/Extracted")
                                Continue()
                                Reset()
                                return
            except Exception as e:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error reading wordlist {white}{file_list}{red}: {str(e)}")
                continue

        if not password_found:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} The entire wordlist has been checked and no passwords match.")
            Continue()
            Reset()

    Slow(decrypted_banner)
    file = ChooseZipRarFile()
    
    # Vérifier si le fichier existe
    if not file or not os.path.exists(file):
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} File not found or not selected: {white}{file}")
        Continue()
        Reset()
    
    # Vérifier si le fichier est un fichier .zip ou .rar
    if not file.lower().endswith(('.zip', '.rar')):
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Selected file is not a .zip or .rar file: {white}{file}")
        Continue()
        Reset()
    
    count = CountEncryptedFiles(file)
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Number of files protected by password: {white + str(count)}")
    if count == 0:
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} No password-protected files found in the archive.")
        Continue()
        Reset()

    Title(f"Password Zip Cracked Attack - File: {file}")

    print(f"""
 {BEFORE}01{AFTER + white} Random Character
 {BEFORE}02{AFTER + white} World List
 """)

    method = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Method -> {white}")

    if method in ["01", "1"]:
        RandomCharacter(count)
    elif method in ["02", "2"]:
        WorldList()
    else:
        ErrorChoice()

except Exception as e:
    Error(e)

