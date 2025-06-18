from Config.Util import *
from Config.Config import *
import os
import platform
import subprocess
import uuid
import ctypes
import random
import re

original_hwid = None
original_mac = {}

def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_current_mac(interface: str) -> str:
    os_name = platform.system().lower()
    try:
        if "windows" in os_name:
            result = subprocess.run(["getmac", "/v", "/fo", "csv"], capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if interface.lower() in line.lower():
                    match = re.search(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})', line, re.IGNORECASE)
                    if match:
                        return match.group(0)
            return "Interface not found or MAC address not available"
        elif "linux" in os_name:
            result = subprocess.run(["cat", f"/sys/class/net/{interface}/address"], capture_output=True, text=True)
            return result.stdout.strip()
        else:
            return "Unsupported operating system"
    except Exception as e:
        return f"Error getting MAC address: {str(e)}"

def get_current_hwid() -> str:
    if platform.system().lower() == "windows":
        try:
            result = subprocess.run(["wmic", "csproduct", "get", "UUID"], capture_output=True, text=True)
            lines = result.stdout.strip().split("\n")
            if len(lines) > 1:
                hwid = lines[1].strip()
                return hwid
            else:
                return "HWID not found"
        except Exception as e:
            return f"Error retrieving HWID: {e}"
    else:
        return "HWID display is not supported on this OS."

def generate_random_mac():
    first_byte = random.choice([0, 2, 4, 6, 8, 'A', 'C', 'E'])
    other_bytes = [format(random.randint(0, 255), '02X') for _ in range(5)]
    return f"{first_byte}2-" + "-".join(other_bytes)

def change_mac_address(interface: str, new_mac: str):
    os_name = platform.system().lower()
    try:
        if "windows" in os_name:
            subprocess.run(["netsh", "interface", "set", "interface", interface, "admin=disable"], capture_output=True)
            reg_path = f"HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Class\\{{4D36E972-E325-11CE-BFC1-08002BE10318}}\\0000"
            subprocess.run(["reg", "add", reg_path, "/v", "NetworkAddress", "/d", new_mac.replace(":", "").replace("-", ""), "/f"], capture_output=True)
            subprocess.run(["netsh", "interface", "set", "interface", interface, "admin=enable"], capture_output=True)
            print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} MAC address change attempted. You may need to disable/enable the network adapter manually.")
        elif "linux" in os_name:
            subprocess.run(["sudo", "ifconfig", interface, "down"], capture_output=True)
            subprocess.run(["sudo", "ifconfig", interface, "hw", "ether", new_mac], capture_output=True)
            subprocess.run(["sudo", "ifconfig", interface, "up"], capture_output=True)
            print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} MAC address changed successfully.")
        else:
            print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Unsupported operating system.")
    except Exception as e:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Error changing MAC address: {e}")

def change_hwid():
    global original_hwid
    if platform.system().lower() == "windows":
        if not is_admin():
            print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Access denied. Please run this script as an administrator.")
            return
        
        if original_hwid is None:
            original_hwid = get_current_hwid()
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Changing HWID :")
        new_hwid = str(uuid.uuid4())
        try:
            subprocess.run(['reg', 'add', r'HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\IDConfigDB\Hardware Profiles\0001', '/v', 'HwProfileGuid', '/d', '{' + new_hwid + '}', '/f'])
            print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} New HWID: {white}{new_hwid}")
        except Exception as e:
            print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Error changing HWID: {e}")
    else:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} HWID spoofing is not supported on this OS.")

def reset_changes():
    global original_hwid, original_mac
    if original_hwid:
        try:
            subprocess.run(['reg', 'add', r'HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\IDConfigDB\Hardware Profiles\0001', '/v', 'HwProfileGuid', '/d', original_hwid, '/f'])
            print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} HWID reset to original value: {white}{original_hwid}")
        except Exception as e:
            print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Error resetting HWID: {e}")

    if original_mac:
        for interface, mac in original_mac.items():
            try:
                change_mac_address(interface, mac)
                print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} MAC Address for {interface} reset to original value: {white}{mac}")
            except Exception as e:
                print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Error resetting MAC Address: {e}")

def show_current_addresses(interface: str):
    global original_mac
    try:
        current_mac = get_current_mac(interface)
        if interface not in original_mac:
            original_mac[interface] = current_mac

        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Current Addresses:{white}\n")
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} MAC Address ({interface}): {white}{current_mac}")
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} HWID: {white}{get_current_hwid()}")
    except Exception as e:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Error displaying current addresses: {e}")

def menu():
    Title("Spoofer")
    
    spoofer_banner = f"""
   ███████╗██████╗  ██████╗  ██████╗ ███████╗███████╗██████╗ 
   ██╔════╝██╔══██╗██╔═══██╗██╔═══██╗██╔════╝██╔════╝██╔══██╗
   ███████╗██████╔╝██║   ██║██║   ██║█████╗  █████╗  ██████╔╝
   ╚════██║██╔═══╝ ██║   ██║██║   ██║██╔══╝  ██╔══╝  ██╔══██╗
   ███████║██║     ╚██████╔╝╚██████╔╝██║     ███████╗██║  ██║
   ╚══════╝╚═╝      ╚═════╝  ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝
    """
    Slow(MainColor2(spoofer_banner))
    
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Bienvenue dans l'outil Spoofer")
    
    while True:
        print(f"\n{white}┌{'─' * 50}┐")
        print(f"{white}│{' ' * 15}Options disponibles{' ' * 17}{white}│")
        print(f"{white}├{'─' * 50}┤")
        print(f"{white}│ {reset}1{green} - Afficher les adresses actuelles{' ' * 13}{white}│")
        print(f"{white}│ {reset}2{green} - Changer l'adresse MAC{' ' * 22}{white}│")
        print(f"{white}│ {reset}3{green} - Changer le HWID (Windows uniquement){' ' * 7}{white}│")
        print(f"{white}│ {reset}4{green} - Réinitialiser les changements{' ' * 16}{white}│")
        print(f"{white}│ {reset}5{green} - Quitter{' ' * 35}{white}│")
        print(f"{white}└{'─' * 50}┘")
        
        choice = input(f"\n{INPUT} Choisissez une option -> {reset}")
        
        if choice == '1':
            interface = input(f"\n{INPUT} Interface réseau (ex: Ethernet, Wi-Fi) -> {reset}")
            show_current_addresses(interface)
            Continue()
        elif choice == '2':
            interface = input(f"\n{INPUT} Interface réseau (ex: Ethernet, Wi-Fi) -> {reset}")
            use_random = input(f"\n{INPUT} Utiliser une adresse MAC aléatoire? (o/n) -> {reset}").lower()
            
            if use_random in ['o', 'oui', 'y', 'yes']:
                new_mac = generate_random_mac()
                print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Adresse MAC aléatoire générée: {white}{new_mac}")
            else:
                new_mac = input(f"\n{INPUT} Nouvelle adresse MAC (format: XX-XX-XX-XX-XX-XX) -> {reset}")
            
            change_mac_address(interface, new_mac)
            Continue()
        elif choice == '3':
            change_hwid()
            Continue()
        elif choice == '4':
            reset_changes()
            Continue()
        elif choice == '5':
            print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Fermeture de l'outil Spoofer...")
            Continue()
            Reset()
            break
        else:
            print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Option invalide. Veuillez réessayer.")
            Continue()

if __name__ == "__main__":
    menu()
