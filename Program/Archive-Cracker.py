from Config.Util import *
from Config.Config import *
from Config.Translates import *
import os
import subprocess

current_language = LANGUAGE

def tr(key):
    return translations[current_language].get(key, key)

def list_wordlists(wordlist_dir):
    if not os.path.exists(wordlist_dir):
        return []
    return [f for f in os.listdir(wordlist_dir) if os.path.isfile(os.path.join(wordlist_dir, f)) and f.endswith('.txt')]

def attempt_crack(archive, password):
    # Use the found 7-Zip path
    cmd = f'"{sevenzip_path}" t -p{password} "{archive}"'
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
    stdout, stderr = process.communicate()
    return "Everything is Ok" in stdout

def main():
    # Check common 7-Zip installation paths
    sevenzip_paths = [
        r"C:\Program Files\7-Zip\7z.exe",
        r"C:\Program Files (x86)\7-Zip\7z.exe",
        r"C:\7-Zip\7z.exe"
    ]
    
    sevenzip_found = False
    for path in sevenzip_paths:
        if os.path.exists(path):
            sevenzip_found = True
            sevenzip_path = path
            break
            
    if not sevenzip_found:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} 7-Zip not found. Please install 7-Zip first.")
        input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press to continue -> " + reset)
        Reset()
    
    archive = input(f"\n{BEFORE + current_time_hour() + AFTER}{INPUT}{primary}Path to archive -> {reset}")
    if not os.path.exists(archive):
        print(f"{BEFORE + current_time_hour() + AFTER} {tr('ArchiveNotFound')}")
        input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press to continue -> " + reset)
        Reset()
    
    wordlist_dir = r"2-Input/Passwords/"

    wordlists = list_wordlists(wordlist_dir)

    if not wordlists:
        print(f"{BEFORE + current_time_hour() + AFTER} {tr('WordlistFound')} {wordlist_dir}")
        input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press to continue -> " + reset)
        Reset()

    print(f"\n{BEFORE + current_time_hour() + AFTER}{WAIT}{primary}Wordlists :\n")
    for index, filename in enumerate(wordlists, start=1):
        print(f"{primary}[{secondary}{index}{primary}] {filename}")

    choice = input(f"\n{INPUT}{primary}{tr('NumWordlist')} -> {reset}")

    try:
        choice = int(choice)
        if 1 <= choice <= len(wordlists):
            wordlist = os.path.join(wordlist_dir, wordlists[choice - 1])
        else:
            ErrorChoice()
    except ValueError:
        print(f"Entrée invalide.")
        input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press to continue -> " + reset)
        Reset()

    if not os.path.exists(wordlist):
        print(f"{BEFORE + current_time_hour() + AFTER} {tr('WordlistNotFound')}")
        input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press to continue -> " + reset)
        Reset()

    print(f"\n{BEFORE + current_time_hour() + AFTER}{WAIT}{primary}Cracking...\n")

    with open(wordlist, 'r') as file:
        for line in file:
            password = line.strip()
            if attempt_crack(archive, password):
                print(f"\n{BEFORE + current_time_hour() + AFTER} {tr('PasswdFound')}: {valid}{password}")
                input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press to continue -> " + reset)
                Reset()
    
    print(f"Shitty wordlist dumbass")
    input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press to continue -> " + reset)
    Reset()

if __name__ == "__main__":
    main()

