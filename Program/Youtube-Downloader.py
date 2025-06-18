# Copyright (c) Your.Tool (https://www.josh-studio.com)
# See the file 'LICENSE' for copying permission
# ----------------------------------------------------------------------------------------------------------------------------------------------------------|
# EN: 
#     - Do not touch or modify the code below. If there is an error, please contact the owner, but under no circumstances should you touch the code.
#     - Do not resell this tool, do not credit it to yours.
# FR: 
#     - Ne pas toucher ni modifier le code ci-dessous. En cas d'erreur, veuillez contacter le propriétaire, mais en aucun cas vous ne devez toucher au code.
#     - Ne revendez pas ce tool, ne le créditez pas au vôtre.

from Program.Config.Config import *
from Program.Config.Util import *
from Program.Config.Translates import *
import os
import time
import re
import requests

current_language = LANGUAGE

def tr(key):
    return translations[current_language].get(key, key)

def is_valid_youtube_url(url):
    # Regex plus précis pour les URLs YouTube
    youtube_patterns = [
        # Format standard watch
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
        # Format court
        r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})',
        # Format embed
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})',
        # Format playlist avec timestamp
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})&list=[a-zA-Z0-9_-]+&t=\d+s?',
        # Format playlist sans timestamp
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})&list=[a-zA-Z0-9_-]+'
    ]
    
    for pattern in youtube_patterns:
        match = re.match(pattern, url)
        if match:
            return match.group(1)  # Retourne l'ID de la vidéo
    return False

def simulate_youtube_download(youtube_url, format_choice, download_path):
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    video_id = is_valid_youtube_url(youtube_url)
    if not video_id:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid YouTube URL format")
        Continue()
        Reset()
    
    # Vérifier si l'URL est accessible
    try:
        response = requests.head(f"https://www.youtube.com/watch?v={video_id}")
        if response.status_code != 200:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Video not accessible or removed")
            Continue()
            Reset()
    except Exception as e:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error checking video: {str(e)}")
        Continue()
        Reset()
    
    # Get "video" title based on video ID (simulated)
    video_title = f"Youtube_Video_{video_id}"
    
    file_format = "mp4" if format_choice == '1' else "mp3"
    output_file = os.path.join(download_path, f"{video_title}.{file_format}")
    
    # Vérifier si le fichier existe déjà
    if os.path.exists(output_file):
        print(f"{BEFORE + current_time_hour() + AFTER} {WARNING} File already exists: {white}{output_file}")
        overwrite = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Overwrite? (y/n) -> {reset}").lower()
        if overwrite != 'y':
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Download cancelled")
            Continue()
            Reset()
    
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Selected format: {white}{file_format}{red}")
    
    if format_choice == '1':  # Video
        print(f"\n{BEFORE + current_time_hour() + AFTER} {WAIT} Available qualities:")
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} 1. 4K (2160p)")
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} 2. HD (1080p)")
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} 3. HD (720p)")
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} 4. SD (480p)")
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} 5. SD (360p)")
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} 6. Low (240p)")
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} 7. Low (144p)")
        
        quality_choice = input(f"\n{BEFORE + current_time_hour() + AFTER} {INPUT} Select quality -> {reset}")
        
        qualities = {
            "1": "4K (2160p)",
            "2": "HD (1080p)",
            "3": "HD (720p)",
            "4": "SD (480p)",
            "5": "SD (360p)",
            "6": "Low (240p)",
            "7": "Low (144p)"
        }
        
        selected_quality = qualities.get(quality_choice, "HD (720p)")
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Selected quality: {white}{selected_quality}{red}")
    else:
        selected_quality = None
    
    # Simuler la progression du téléchargement
    total_size = 25 * 1024 * 1024  # Simuler une taille de fichier de 25MB pour vidéo, 5MB pour audio
    if format_choice == '2':
        total_size = 5 * 1024 * 1024
        
    downloaded = 0
    chunk_size = total_size // 20
    
    for i in range(20):
        downloaded += chunk_size
        percent = (downloaded / total_size) * 100
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Downloading... {white}{percent:.1f}%{red}")
        time.sleep(0.2)
    
    # Créer un fichier vide pour simuler le téléchargement
    with open(output_file, 'w') as f:
        f.write(f"This is a placeholder for a YouTube {file_format} file.\n")
        f.write(f"The actual functionality would download the {file_format} from: {youtube_url}\n")
        if format_choice == '1':
            f.write(f"Selected quality: {selected_quality}\n")
    
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Download complete!")
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} File saved to: {white}{output_file}{red}")
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Note: This is a simulated download. To implement actual YouTube downloads,")
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} you would need to use a specialized library like youtube-dl or pytube.")
    
    input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press to continue -> " + reset)
    Reset()

def main():
    try:
        Clear()
        Title("Youtube Downloader")
        
        print(f"\n{BEFORE + current_time_hour() + AFTER} {WAIT} Youtube Downloader\n")
        
        youtube_url = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Enter Youtube URL -> {reset}")
        
        if not is_valid_youtube_url(youtube_url):
            ErrorUrl()
        
        print(f"\n{BEFORE + current_time_hour() + AFTER} {WAIT} Download options:")
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} 1. Video")
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} 2. Audio only")
        
        format_choice = input(f"\n{BEFORE + current_time_hour() + AFTER} {INPUT} Select format -> {reset}")
        
        if format_choice not in ['1', '2']:
            ErrorChoice()
        
        download_path = os.path.join(tool_path, "1-Output", "Youtube-Downloads")
        
        simulate_youtube_download(youtube_url, format_choice, download_path)
    except Exception as e:
        Error(e)

if __name__ == "__main__":
    main()


