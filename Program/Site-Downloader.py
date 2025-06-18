from Config.Util import *
from Config.Config import *
from Config.Translates import *
import subprocess
import os
import shutil
import requests
import sys
import ctypes
import time
import zipfile
import platform
import random
import string

current_language = LANGUAGE

def tr(key):
    return translations[current_language].get(key, key)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def check_wget_installed():
    """Vérifie si wget est installé sur le système"""
    return shutil.which("wget") is not None

def check_httrack_installed():
    """Vérifie si HTTrack est installé sur le système"""
    try:
        # Essayer avec la commande système
        result = subprocess.run(['httrack', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_wget():
    """Télécharge et installe wget"""
    try:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} Téléchargement de wget en cours...")
        
        # Chemin pour wget dans le dossier de l'application
        app_wget_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "wget.exe")
        
        # Télécharger wget
        wget_url = "https://eternallybored.org/misc/wget/1.21.3/64/wget.exe"
        response = requests.get(wget_url)
        
        # Sauvegarder wget dans le dossier de l'application
        with open(app_wget_path, 'wb') as f:
            f.write(response.content)
        
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} wget a été installé avec succès!")
        return True
    except Exception as e:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR}{primary} Erreur lors de l'installation de wget: {e}")
        return False

def download_site():
    url = input(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} {tr('Website_url')} -> {reset}").strip()
    
    if not url.startswith('http'):
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} {tr('ErrorURL')}")
        input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press to continue -> " + reset)
        Reset()
        return
    
    # Créer le répertoire de sortie
    output_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "1-Output", "Sites")
    os.makedirs(output_directory, exist_ok=True)
    
    # Nom du site basé sur l'URL (sans http:// ou https://)
    site_name = url.replace("https://", "").replace("http://", "").replace("/", "_").replace(".", "_")
    site_output_dir = os.path.join(output_directory, site_name)
    
    # Demander à l'utilisateur quelle méthode utiliser
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} Choisissez la méthode de téléchargement:")
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} 1 - Basique (wget - rapide mais peut manquer du contenu JavaScript)")
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} 2 - Super (wget avec options avancées - pour les sites dynamiques)")
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} 3 - Ultra (wget avec options très avancées - pour les sites complexes)")
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} 4 - Extreme (optimisé pour les sites Next.js/React comme aamirshaikh.net)")
    
    method = input(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} Méthode (1/2/3/4) -> {reset}").strip()
    
    if method == "1":
        download_with_wget(url, site_output_dir)
    elif method == "2":
        download_with_wget_super(url, site_output_dir)
    elif method == "3":
        download_with_wget_advanced(url, site_output_dir)
    elif method == "4":
        download_with_wget_extreme(url, site_output_dir)
    else:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR}{primary} Choix invalide.")
        input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press to continue -> " + reset)
        Reset()
        return

def download_with_wget(url, output_dir):
    # Vérifier si wget est installé, sinon l'installer
    wget_path = "wget"
    if not check_wget_installed():
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} wget n'est pas installé, tentative d'installation automatique...")
        if install_wget():
            # Utiliser le chemin local pour wget
            wget_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "wget.exe")
        else:
            print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR}{primary} Impossible d'installer wget automatiquement.")
            print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} Veuillez télécharger wget manuellement depuis https://eternallybored.org/misc/wget/")
            input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press to continue -> " + reset)
            Reset()
            return
    
    # Commande wget standard
    wget_command = [
        wget_path,
        "--mirror",
        "--convert-links",
        "--adjust-extension",
        "--page-requisites",
        "--no-parent",
        url,
        "-P", output_dir
    ]
    
    try:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} Téléchargement en cours avec wget... Cela peut prendre un moment.")
        subprocess.run(wget_command, check=True)
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} {tr('1SiteDownload')} {secondary}{url}{primary} {tr('2SiteDownload')} {secondary}{output_dir}{primary}.")
        input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press to continue -> " + reset)
        Reset()
    except subprocess.CalledProcessError as e:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR}{primary} {tr('ErrorDownloadSite')} {e}")
        input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press to continue -> " + reset)
        Reset()
    except Exception as e:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR}{primary} Erreur inattendue: {e}")
        input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press to continue -> " + reset)
        Reset()

def download_with_wget_super(url, output_dir):
    # Vérifier si wget est installé, sinon l'installer
    wget_path = "wget"
    if not check_wget_installed():
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} wget n'est pas installé, tentative d'installation automatique...")
        if install_wget():
            # Utiliser le chemin local pour wget
            wget_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "wget.exe")
        else:
            print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR}{primary} Impossible d'installer wget automatiquement.")
            print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} Veuillez télécharger wget manuellement depuis https://eternallybored.org/misc/wget/")
            input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press to continue -> " + reset)
            Reset()
            return
    
    # Options super pour wget
    wget_command = [
        wget_path,
        "--mirror",
        "--convert-links",
        "--adjust-extension",
        "--page-requisites",
        "--span-hosts",  # Autorise la récupération depuis d'autres domaines (CDN, etc.)
        "--domains=" + url.replace("https://", "").replace("http://", "").split('/')[0],  # Limite aux domaines liés
        "--recursive",
        "--level=3",  # Profondeur de récursion
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "--no-parent",
        url,
        "-P", output_dir
    ]
    
    try:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} Téléchargement en cours avec wget (mode super)... Cela peut prendre un moment.")
        subprocess.run(wget_command, check=True)
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} Site {secondary}{url}{primary} téléchargé dans {secondary}{output_dir}{primary}.")
        input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press to continue -> " + reset)
        Reset()
    except subprocess.CalledProcessError as e:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR}{primary} Erreur lors du téléchargement: {e}")
        input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press to continue -> " + reset)
        Reset()
    except Exception as e:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR}{primary} Erreur inattendue: {e}")
        input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press to continue -> " + reset)
        Reset()

def download_with_wget_advanced(url, output_dir):
    # Vérifier si wget est installé, sinon l'installer
    wget_path = "wget"
    if not check_wget_installed():
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} wget n'est pas installé, tentative d'installation automatique...")
        if install_wget():
            # Utiliser le chemin local pour wget
            wget_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "wget.exe")
        else:
            print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR}{primary} Impossible d'installer wget automatiquement.")
            print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} Veuillez télécharger wget manuellement depuis https://eternallybored.org/misc/wget/")
            input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press to continue -> " + reset)
            Reset()
            return
    
    # Options avancées pour wget
    wget_command = [
        wget_path,
        "--mirror",
        "--convert-links",
        "--adjust-extension",
        "--page-requisites",
        "--span-hosts",  # Autorise la récupération depuis d'autres domaines (CDN, etc.)
        "--domains=" + url.replace("https://", "").replace("http://", "").split('/')[0],  # Limite aux domaines liés
        "--include-directories=*",
        "--recursive",
        "--level=5",  # Profondeur de récursion plus élevée
        "--reject=.git*",
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "--random-wait",  # Ajoute des délais aléatoires
        "--wait=1",  # Délai minimal d'une seconde
        "--execute=robots=off",  # Ignore robots.txt
        "--timeout=60",  # Timeout plus long
        "--tries=5",  # Plus de tentatives
        "--no-parent",
        "--continue",  # Permet de reprendre les téléchargements interrompus
        "--retry-connrefused",  # Réessaie même si la connexion est refusée
        "--no-check-certificate",  # Ignore les problèmes de certificats
        url,
        "-P", output_dir
    ]
    
    try:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} Téléchargement avancé en cours... Cela peut prendre beaucoup de temps.")
        # Utiliser run sans check=True pour éviter que le programme s'arrête en cas d'erreur
        result = subprocess.run(wget_command, stderr=subprocess.PIPE, text=True)
        
        if result.returncode != 0:
            print(f"\n{BEFORE + current_time_hour() + AFTER} {WARNING}{primary} Le téléchargement a rencontré des erreurs, mais des fichiers ont peut-être été téléchargés.")
            print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} Essai avec des options simplifiées...")
            
            # Nouvelle tentative avec des options simplifiées
            simple_command = [
                wget_path,
                "--recursive",
                "--level=3",
                "--convert-links",
                "--page-requisites",
                "--no-clobber",
                "--continue",
                "--no-check-certificate",
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                url,
                "-P", output_dir
            ]
            subprocess.run(simple_command)
        
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} Site {secondary}{url}{primary} téléchargé dans {secondary}{output_dir}{primary}.")
        input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press to continue -> " + reset)
        Reset()
    except subprocess.CalledProcessError as e:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR}{primary} Erreur lors du téléchargement: {e}")
        input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press to continue -> " + reset)
        Reset()
    except Exception as e:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR}{primary} Erreur inattendue: {e}")
        input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press to continue -> " + reset)
        Reset()

def download_with_wget_extreme(url, output_dir):
    """Mode extrême optimisé pour les sites Next.js/React comme aamirshaikh.net"""
    # Vérifier si wget est installé, sinon l'installer
    wget_path = "wget"
    if not check_wget_installed():
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} wget n'est pas installé, tentative d'installation automatique...")
        if install_wget():
            # Utiliser le chemin local pour wget
            wget_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "wget.exe")
        else:
            print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR}{primary} Impossible d'installer wget automatiquement.")
            print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} Veuillez télécharger wget manuellement depuis https://eternallybored.org/misc/wget/")
            input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press to continue -> " + reset)
            Reset()
            return
    
    # Extraire le domaine principal
    domain = url.replace("https://", "").replace("http://", "").split('/')[0]
    
    # Configuration commune pour wget
    common_options = [
        "--no-check-certificate",  # Ignorer les problèmes de certificats
        "--content-on-error",      # Continuer même en cas d'erreur HTTP
        "--retry-connrefused",     # Réessayer même si la connexion est refusée
        "--no-cache",             # Ne pas utiliser le cache
        "--no-cookies",           # Ne pas utiliser les cookies
        "--timeout=15",           # Timeout plus court mais plus de retries
        "--tries=5",             # Plus de tentatives
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "--header=Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "--header=Accept-Language: fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
        "--header=Accept-Encoding: gzip, deflate, br",
        "--header=Connection: keep-alive",
        "--header=Upgrade-Insecure-Requests: 1"
    ]
    
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} Tentative de téléchargement direct de la page principale...")
    
    # Première tentative - Téléchargement direct de la page principale
    initial_command = [
        wget_path,
        *common_options,
        "--page-requisites",      # Télécharger tous les fichiers nécessaires
        "--span-hosts",          # Autoriser les domaines externes
        "--convert-links",       # Convertir les liens pour une utilisation locale
        url,
        "-P", output_dir
    ]
    
    try:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} Téléchargement de la page principale...")
        result = subprocess.run(initial_command, capture_output=True, text=True)
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} Sortie de wget: {result.stdout}")
        if result.stderr:
            print(f"\n{BEFORE + current_time_hour() + AFTER} {WARNING}{primary} Erreurs wget: {result.stderr}")
    except Exception as e:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR}{primary} Erreur lors du téléchargement initial: {str(e)}")
    
    # Liste des chemins spécifiques à Next.js
    nextjs_paths = [
        "/_next/static/chunks/main",
        "/_next/static/chunks/pages",
        "/_next/static/chunks/framework",
        "/_next/static/chunks/webpack",
        "/_next/static/css",
        "/_next/static/media",
        "/_next/data",
        "/api",
        "/static",
        "/assets"
    ]
    
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} Téléchargement des ressources Next.js...")
    
    for path in nextjs_paths:
        try:
            specific_url = url.rstrip('/') + path
            print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} Tentative sur: {specific_url}")
            
            specific_command = [
                wget_path,
                *common_options,
                "--recursive",
                "--level=2",
                "--no-parent",
                "--reject-regex", "(.*\\?[^&]*source=)[^&]*",  # Ignorer les URLs avec des paramètres source
                specific_url,
                "-P", output_dir
            ]
            
            result = subprocess.run(specific_command, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"\n{BEFORE + current_time_hour() + AFTER} {WARNING}{primary} Avertissement pour {path}: {result.stderr}")
        except Exception as e:
            print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR}{primary} Erreur pour {path}: {str(e)}")
            continue
    
    # Tentative finale avec des options plus agressives
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} Tentative finale avec des options plus agressives...")
    
    final_command = [
        wget_path,
        *common_options,
        "--recursive",
        "--level=3",
        "--page-requisites",
        "--span-hosts",
        "--convert-links",
        "--adjust-extension",
        "--no-parent",
        "--domains=" + domain,
        "--reject-regex", "(.*\\?[^&]*source=)[^&]*",
        url,
        "-P", output_dir
    ]
    
    try:
        subprocess.run(final_command, capture_output=True, text=True)
    except Exception as e:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR}{primary} Erreur lors de la tentative finale: {str(e)}")
    
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} Site {secondary}{url}{primary} téléchargé dans {secondary}{output_dir}{primary}.")
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} Le téléchargement en mode extrême est terminé!")
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{primary} Note: Certains fichiers peuvent ne pas avoir été téléchargés en raison des protections du site.")
    input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press to continue -> " + reset)
    Reset()

if __name__ == "__main__":
    download_site()

