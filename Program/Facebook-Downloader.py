from Config.Util import *
from Config.Config import *
from Config.Translates import *
import yt_dlp
import os
import re

current_language = LANGUAGE

def tr(key):
    return translations[current_language].get(key, key)

def is_valid_facebook_url(url):
    # Regex pour valider les URLs Facebook
    facebook_patterns = [
        r'(?:https?://)?(?:www\.)?facebook\.com/[^/]+/videos/\d+',
        r'(?:https?://)?(?:www\.)?facebook\.com/watch/\?v=\d+',
        r'(?:https?://)?(?:www\.)?fb\.watch/[^/]+',
        r'(?:https?://)?(?:www\.)?facebook\.com/[^/]+/posts/\d+'
    ]
    return any(re.match(pattern, url) for pattern in facebook_patterns)

def télécharger_vidéo_facebook(url):
    try:
        if not is_valid_facebook_url(url):
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid Facebook video URL")
            Continue()
            Reset()
            return
            
        download_dir = os.path.join("1-Output", "VideoDownload", "Facebook")
        os.makedirs(download_dir, exist_ok=True)

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'extract_flat': False,
            'socket_timeout': 30,
            'retries': 3,
            'ignoreerrors': True,
            'nooverwrites': True,
            'cookiefile': None,  # Pas de cookies nécessaires pour Facebook
            'nocheckcertificate': True,  # Ignorer les erreurs de certificat
            'progress_hooks': [lambda d: print(f"{BEFORE + current_time_hour() + AFTER} {INFO} {d.get('status', '')}: {d.get('_percent_str', '0%')}")],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                if info:
                    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Found video: {white}{info.get('title', 'Unknown title')}")
                    if os.path.exists(os.path.join(download_dir, f"{info.get('title', 'video')}.mp4")):
                        overwrite = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} File already exists. Overwrite? (y/n) -> {reset}").lower()
                        if overwrite != 'y':
                            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Download cancelled")
                            Continue()
                            Reset()
                            return
                    ydl.download([url])
                    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} {tr('DownloadDone')}")
                else:
                    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Could not find video information")
            except Exception as e:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Download error: {str(e)}")
        Continue()
        Reset()
    except Exception as e:
        Error(e)

if __name__ == "__main__":
    url = input(f"\n{primary}{INPUT} {tr('URLVideo')} -> {reset}")
    télécharger_vidéo_facebook(url)

