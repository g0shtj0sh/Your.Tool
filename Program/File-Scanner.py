from Config.Util import *
from Config.Config import *
from Config.Translates import *
import requests
import time
import sys
import os

current_language = LANGUAGE

Slow(scan_banner)

def tr(key):
    return translations[current_language].get(key, key)

def load_api_key(file_path):
    try:
        if not os.path.exists(file_path):
            print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Le fichier de clé API n'existe pas : {file_path}")
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Veuillez créer le fichier avec votre clé API VirusTotal")
            Continue()
            Reset()
            return None
            
        with open(file_path, 'r') as file:
            api_key = file.read().strip()
            
        if not api_key:
            print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Le fichier de clé API est vide")
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Veuillez ajouter votre clé API VirusTotal dans le fichier")
            Continue()
            Reset()
            return None
            
        return api_key
    except Exception as e:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Erreur lors de la lecture de la clé API : {e}")
        Continue()
        Reset()
        return None

def upload_file_to_virustotal(file_path, api_key):
    url = 'https://www.virustotal.com/api/v3/files'
    headers = {
        'x-apikey': api_key
    }
    
    # Vérifier si le fichier existe
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Le fichier {file_path} n'existe pas")
        
    # Vérifier la taille du fichier (limite de 32MB pour VirusTotal)
    if os.path.getsize(file_path) > 32 * 1024 * 1024:
        raise ValueError("Le fichier est trop volumineux (limite de 32MB)")
    
    try:
        with open(file_path, 'rb') as file:
            files = {'file': (os.path.basename(file_path), file)}
            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
            response_data = response.json()
            
            if 'data' not in response_data or 'id' not in response_data['data']:
                raise ValueError("Réponse invalide de VirusTotal")
                
            return response_data['data']['id']
    except requests.exceptions.RequestException as e:
        if response.status_code == 401:
            raise ValueError("Clé API VirusTotal invalide")
        elif response.status_code == 429:
            raise ValueError("Limite de requêtes VirusTotal atteinte")
        else:
            raise ValueError(f"Erreur lors de l'upload : {str(e)}")
    except Exception as e:
        raise ValueError(f"Erreur inattendue : {str(e)}")

def get_analysis_results(file_id, api_key):
    url = f'https://www.virustotal.com/api/v3/analyses/{file_id}'
    headers = {
        'x-apikey': api_key
    }
    while True:
        response = requests.get(url, headers=headers)
        response_data = response.json()
        if response_data['data']['attributes']['status'] == 'completed':
            return response_data
        time.sleep(10)

def display_detailed_results(analysis_results):
    stats = analysis_results['data']['attributes']['stats']
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} Scan results for file:\n")
    print(f"{primary}Harmless: {secondary}{stats['harmless']}")
    print(f"{primary}Malicious: {secondary}{stats['malicious']}")
    print(f"{primary}Suspicious: {secondary}{stats['suspicious']}")
    print(f"{primary}Undetected: {secondary}{stats['undetected']}\n")

    if stats['malicious'] > 0:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} The following antivirus engines detected the file as malicious:\n")
        scans = analysis_results['data']['attributes']['results']
        for engine, result in scans.items():
            if result['category'] == 'malicious':
                print(f"{primary}{engine}: {result['result']}")

def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1].strip()
    else:
        file_path = input(f"\n{BEFORE + current_time_hour() + AFTER} {INPUT} Path to file to scan -> {secondary}").strip()
    
    if not os.path.isfile(file_path):
        print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Le fichier spécifié n'existe pas ou n'est pas un fichier valide.")
        Continue()
        Reset()
        return

    api_key = load_api_key('2-Input/FileCheck/apikey.txt')
    if not api_key:
        return

    try:
        file_id = upload_file_to_virustotal(file_path, api_key)
        print(f"\n{BEFORE + current_time_hour() + AFTER} {WAIT} File uploaded successfully. Waiting for analysis...{secondary}")
        analysis_results = get_analysis_results(file_id, api_key)
        display_detailed_results(analysis_results)
        Continue()
        Reset()

    except Exception as e:
        print(f"{BEFORE + current_time_hour() + AFTER}{ERROR}{primary} An error occurred: {e}")
        Continue()
        Reset()

if __name__ == "__main__":
    main()

