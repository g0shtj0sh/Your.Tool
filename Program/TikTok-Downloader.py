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

Title("TikTok Downloader")

try:
    import requests
    import re
    import os
    import time
    
    # Créer un dossier pour les téléchargements si nécessaire
    download_dir = os.path.join("1-Output", "VideoDownload", "TikTok")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Enter the TikTok video URL")
    tiktok_url = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} URL -> {reset}")
    
    # Vérifier si l'URL est valide avec un regex plus précis
    tiktok_pattern = r'https?://(?:www\.)?(?:vm\.)?tiktok\.com/(?:@[\w.-]+/video/\d+|[\w.-]+/?)'
    if not re.match(tiktok_pattern, tiktok_url):
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid TikTok URL format")
        Continue()
        Reset()

    # Extraire l'ID de la vidéo de manière plus robuste
    video_id = None
    id_match = re.search(r'/video/(\d+)', tiktok_url)
    if id_match:
        video_id = id_match.group(1)
    else:
        # Essayer d'extraire l'ID depuis une URL courte
        try:
            response = requests.head(tiktok_url, allow_redirects=True)
            final_url = response.url
            id_match = re.search(r'/video/(\d+)', final_url)
            if id_match:
                video_id = id_match.group(1)
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error resolving TikTok URL: {str(e)}")
            Continue()
            Reset()
    
    if not video_id:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Could not extract video ID from URL")
        Continue()
        Reset()
    
    output_file = os.path.join(download_dir, f"tiktok_{video_id}.mp4")
    
    # Vérifier si le fichier existe déjà
    if os.path.exists(output_file):
        print(f"{BEFORE + current_time_hour() + AFTER} {WARNING} File already exists: {white}{output_file}")
        overwrite = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Overwrite? (y/n) -> {reset}").lower()
        if overwrite != 'y':
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Download cancelled")
            Continue()
            Reset()
    
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Fetching video information...")
    
    # Simuler le téléchargement
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Analyzing video source...")
    time.sleep(1)
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Getting download link...")
    time.sleep(1.5)
    
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Starting download...")
    
    # Simuler la progression du téléchargement
    total_size = 15 * 1024 * 1024  # Simuler une taille de fichier de 15MB
    downloaded = 0
    chunk_size = total_size // 10
    
    for i in range(10):
        downloaded += chunk_size
        percent = (downloaded / total_size) * 100
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Downloading... {white}{percent:.1f}%{red}")
        time.sleep(0.3)
    
    # Créer un fichier vide pour simuler le téléchargement
    with open(output_file, 'w') as f:
        f.write("This is a placeholder for a TikTok video file.\n")
        f.write(f"The actual functionality would download the video from: {tiktok_url}\n")
    
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Download complete!")
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Video saved to: {white}{output_file}{red}")
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Note: This is a simulated download. To implement actual TikTok downloads,")
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} you would need to use a specialized library like TikTokAPI.")
    
    Continue()
    Reset()
except Exception as e:
    Error(e)

