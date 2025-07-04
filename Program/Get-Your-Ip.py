from Config.Util import *
from Config.Config import *
from Config.Translates import *

current_language = LANGUAGE

def tr(key):
    return translations[current_language].get(key, key)

try:
    from json import *
    import requests
    import socket
    if sys.platform.startswith("win"):
        "WINDOWS"
        import win32api
    else:
        pass
except Exception as e:
   ErrorModule(e)
   
Title("Get Your Ip")

try:
    print(f"\n{BEFORE + current_time_hour() + AFTER} {WAIT} {tr('IpSearch')}")
    try:
        hostname_pc = socket.gethostname()
    except:
        hostname_pc = "None"

    try:
        username_pc = os.getlogin()
    except:
        username_pc = "None"

    try:
        if sys.platform.startswith("win"):
            "WINDOWS"
            displayname_pc = win32api.GetUserNameEx(win32api.NameDisplay)
        else:
            displayname_pc = "None"
    except:
        displayname_pc = "None"

    try:
        response = requests.get(f'https://{website}/api/ip/myip')
        ip_address_public = response.json()['ip']
    except:
        ip_address_public = "None"

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))  

        ip_address_local = s.getsockname()[0]
        s.close()
    except:
        ip_address_local = "None"

    try:
        ip_address_ipv6 = []
        all_interfaces = socket.getaddrinfo(socket.gethostname(), None)
        for interface in all_interfaces:
            if interface[0] == socket.AF_INET6:
                ip_address_ipv6.append(interface[4][0])
        ip_address_ipv6 = ' / '.join(ip_address_ipv6)
    except:
            ip_address_ipv6 = "None"

    print(f"""
  {INFO_ADD} {tr('PCHostname')}      : {secondary}{hostname_pc}{primary}
  {INFO_ADD} {tr('PCUsername')}    : {secondary}{username_pc}{primary}
  {INFO_ADD} {tr('PCDisplayName')}   : {secondary}{displayname_pc}{primary}
  {INFO_ADD} {tr('IpPublic')} : {secondary}{ip_address_public}{primary}
  {INFO_ADD} {tr('Iplocal')} : {secondary}{ip_address_local}{primary}
  {INFO_ADD} {tr('Ipv6')}               : {secondary}{ip_address_ipv6}{primary}
    """)

    Continue()
    Reset()
except Exception as e:
    Error(e)
