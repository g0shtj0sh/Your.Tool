# Copyright (c) Your.Tool (https://www.josh-studio.com)
# See the file 'LICENSE' for copying permission
# ----------------------------------------------------------------------------------------------------------------------------------------------------------|
# EN: 
#     - Do not touch or modify the code below. If there is an error, please contact the owner, but under no circumstances should you touch the code.
#     - Do not resell this tool, do not credit it to yours.
# FR: 
#     - Ne pas toucher ni modifier le code ci-dessous. En cas d'erreur, veuillez contacter le propriétaire, mais en aucun cas vous ne devez toucher au code.
#     - Ne revendez pas ce tool, ne le créditez pas au vôtre.

from Config.Util import *
from Config.Config import *
try:
    import socket
    import ssl
    import subprocess
    import sys
    import requests
    from requests.exceptions import RequestException
    import concurrent.futures
    import re
    import json
    import dns.resolver
except Exception as e:
    ErrorModule(e)
    
Title("Ip Scanner")

try:
    def validate_ip(ip):
        """Valide et normalise l'adresse IP"""
        # Regex pour IPv4
        ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        # Regex pour IPv6
        ipv6_pattern = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|^::$|^::1$|^([0-9a-fA-F]{1,4}:){1,7}:$|^:([0-9a-fA-F]{1,4}:){1,6}:$'
        
        if not ip:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} IP invalide : l'IP ne peut pas être vide")
            return None
            
        # Vérification IPv4
        if re.match(ipv4_pattern, ip):
            try:
                # Vérifie que chaque octet est entre 0 et 255
                octets = ip.split('.')
                if all(0 <= int(octet) <= 255 for octet in octets):
                    return ip
            except ValueError:
                pass
                
        # Vérification IPv6
        elif re.match(ipv6_pattern, ip):
            return ip
            
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} IP invalide : format incorrect")
        return None

    def IpType(ip):
        ip_type = "Unknown"
        if ':' in ip:
            ip_type = "ipv6"
        elif '.' in ip:
            ip_type = "ipv4"
        print(f"{BEFORE + current_time_hour() + AFTER} {ADD} IP Type: {white}{ip_type}{red}")
        return ip_type

    def IpPing(ip, ip_type):
        try:
            if sys.platform.startswith("win"):
                ping_cmd = ['ping', '-n', '1', ip]
            else:
                ping_cmd = ['ping', '-c', '1', '-W', '1']
                if ip_type == "ipv6":
                    ping_cmd.append('-6')
                ping_cmd.append(ip)
                
            result = subprocess.run(ping_cmd, capture_output=True, text=True, timeout=2)
            
            if result.returncode == 0:
                # Extraction du temps de réponse
                if sys.platform.startswith("win"):
                    time_match = re.search(r'temps=(\d+)ms', result.stdout)
                else:
                    time_match = re.search(r'time=(\d+\.\d+) ms', result.stdout)
                    
                if time_match:
                    response_time = time_match.group(1)
                    print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Ping: {white}Succeed{red} Response Time: {white}{response_time}ms{red}")
                else:
                    print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Ping: {white}Succeed{red}")
            else:
                print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Ping: {white}Failed{red}")
                
        except subprocess.TimeoutExpired:
            print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Ping: {white}Timeout{red}")
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Erreur de ping : {str(e)}")

    def IpPort(ip, ip_type):
        common_ports = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 69: "TFTP",
            80: "HTTP", 110: "POP3", 123: "NTP", 143: "IMAP", 194: "IRC", 389: "LDAP",
            443: "HTTPS", 161: "SNMP", 3306: "MySQL", 5432: "PostgreSQL", 6379: "Redis",
            1521: "Oracle DB", 3389: "RDP", 8080: "HTTP-Alt", 8443: "HTTPS-Alt",
            9000: "Portainer", 9090: "Prometheus", 27017: "MongoDB", 6379: "Redis",
            11211: "Memcached", 5601: "Kibana", 9200: "Elasticsearch", 9300: "Elasticsearch-Cluster"
        }
        
        def scan_port(ip, port):
            try:
                # Utilise le bon type de socket selon l'IP
                addr_family = socket.AF_INET6 if ip_type == "ipv6" else socket.AF_INET
                with socket.socket(addr_family, socket.SOCK_STREAM) as sock:
                    sock.settimeout(1)
                    result = sock.connect_ex((ip, port))
                    if result == 0:
                        service_info = ""
                        try:
                            if port in [80, 443, 8080, 8443]:
                                # Tentative de bannière HTTP
                                protocol = "https" if port in [443, 8443] else "http"
                                response = requests.get(f"{protocol}://{ip}:{port}", timeout=2, verify=False)
                                server = response.headers.get('Server', '')
                                if server:
                                    service_info = f" - Server: {server}"
                            elif port == 22:
                                # Tentative de bannière SSH
                                with socket.socket(addr_family, socket.SOCK_STREAM) as ssh_sock:
                                    ssh_sock.settimeout(2)
                                    ssh_sock.connect((ip, port))
                                    banner = ssh_sock.recv(1024).decode().strip()
                                    if banner:
                                        service_info = f" - Banner: {banner}"
                        except:
                            pass
                        print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Port: {white}{port}{red} Status: {white}Open{red} Protocol: {white}{common_ports.get(port, 'Unknown')}{service_info}{red}")
            except Exception:
                pass
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(lambda p: scan_port(ip, p), common_ports.keys())

    def IpDns(ip, ip_type):
        try:
            dns_info = socket.gethostbyaddr(ip)
            hostname = dns_info[0]
            aliases = dns_info[1]
            addresses = dns_info[2]
            
            print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Hostname: {white}{hostname}{red}")
            
            if aliases:
                print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Aliases: {white}{', '.join(aliases)}{red}")
                
            if addresses:
                print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Additional IP Addresses: {white}{', '.join(addresses)}{red}")
                
            # Tentative de résolution DNS inverse
            try:
                resolver = dns.resolver.Resolver()
                # Conversion de l'IP en format arpa pour la recherche PTR
                if ip_type == "ipv4":
                    arpa = '.'.join(reversed(ip.split('.'))) + '.in-addr.arpa'
                else:  # ipv6
                    expanded_ip = ipaddress.IPv6Address(ip).exploded
                    arpa = '.'.join(reversed(expanded_ip.replace(':', ''))) + '.ip6.arpa'
                    
                ptr_records = resolver.resolve(arpa, 'PTR')
                for rdata in ptr_records:
                    print(f"{BEFORE + current_time_hour() + AFTER} {ADD} PTR Record: {white}{str(rdata)}{red}")
            except Exception:
                pass
                
        except socket.herror as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Erreur DNS : {str(e)}")

    def IpHostInfo(ip):
        try:
            api_url = f"https://ipinfo.io/{ip}/json"
            response = requests.get(api_url, timeout=5)
            api = response.json()
            
            # Informations de base
            for key in ['country', 'region', 'city', 'loc', 'timezone', 'org', 'asn', 'hostname']:
                if key in api:
                    print(f"{BEFORE + current_time_hour() + AFTER} {ADD} {key.capitalize()}: {white}{api[key]}{red}")
                    
            # Informations de localisation détaillées
            if 'loc' in api:
                lat, lon = api['loc'].split(',')
                print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Latitude: {white}{lat}{red}")
                print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Longitude: {white}{lon}{red}")
                
            # Informations sur l'AS
            if 'asn' in api:
                try:
                    asn_response = requests.get(f"https://ipinfo.io/{api['asn']}/json", timeout=5)
                    asn_data = asn_response.json()
                    if 'name' in asn_data:
                        print(f"{BEFORE + current_time_hour() + AFTER} {ADD} ASN Name: {white}{asn_data['name']}{red}")
                    if 'type' in asn_data:
                        print(f"{BEFORE + current_time_hour() + AFTER} {ADD} ASN Type: {white}{asn_data['type']}{red}")
                except:
                    pass
                    
            # Informations de confidentialité
            if 'privacy' in api:
                privacy = api['privacy']
                if isinstance(privacy, dict):
                    for key, value in privacy.items():
                        if value:
                            print(f"{BEFORE + current_time_hour() + AFTER} {WARNING} Privacy: {white}{key}{red}")
                            
            # Informations d'abus
            if 'abuse' in api:
                abuse = api['abuse']
                if isinstance(abuse, dict):
                    for key, value in abuse.items():
                        print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Abuse {key}: {white}{value}{red}")
                        
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Erreur lors de la récupération des informations : {str(e)}")

    def SslCertificateCheck(ip, ip_type):
        try:
            context = ssl.create_default_context()
            with socket.create_connection((ip, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=ip) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Informations de base
                    print(f"{BEFORE + current_time_hour() + AFTER} {ADD} SSL Version: {white}{ssock.version()}{red}")
                    print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Cipher: {white}{ssock.cipher()[0]}{red}")
                    
                    # Informations du certificat
                    if 'subject' in cert:
                        subject = dict(x[0] for x in cert['subject'])
                        print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Certificate Subject: {white}{subject}{red}")
                        
                    if 'issuer' in cert:
                        issuer = dict(x[0] for x in cert['issuer'])
                        print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Certificate Issuer: {white}{issuer}{red}")
                        
                    if 'notBefore' in cert:
                        print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Valid From: {white}{cert['notBefore']}{red}")
                        
                    if 'notAfter' in cert:
                        print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Valid Until: {white}{cert['notAfter']}{red}")
                        
                    if 'subjectAltName' in cert:
                        alt_names = [x[1] for x in cert['subjectAltName'] if x[0].lower() == 'dns']
                        print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Alternative Names: {white}{', '.join(alt_names)}{red}")
                        
        except ssl.SSLError as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Erreur SSL : {str(e)}")
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Erreur lors de la vérification du certificat : {str(e)}")

    Slow(scan_banner)
    ip = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Ip -> {reset}")
    
    # Validation de l'IP
    ip = validate_ip(ip)
    if not ip:
        Continue()
        Reset()
    else:
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Information Recovery..{reset}")
        print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Ip: {white}{ip}{red}")
        
        ip_type = IpType(ip)
        IpPing(ip, ip_type)
        IpDns(ip, ip_type)
        IpPort(ip, ip_type)
        IpHostInfo(ip)
        if ip_type == "ipv4":  # SSL check only for IPv4
            SslCertificateCheck(ip, ip_type)
        Continue()
        Reset()

except Exception as e:
    Error(e)
