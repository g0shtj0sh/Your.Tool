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
    import concurrent.futures
    import requests
    from urllib.parse import urlparse
    import ssl
    import urllib3
    from requests.exceptions import RequestException
    import time
    import re
    import dns.resolver
    from bs4 import BeautifulSoup
    import whois
    import json
except Exception as e:
    ErrorModule(e)

Title("Website Scanner")

try:
    user_agent = ChoiceUserAgent()
    headers = {"User-Agent": user_agent}

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    def validate_url(url):
        """Valide et normalise l'URL"""
        if not url:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} URL invalide : l'URL ne peut pas être vide")
            return None
            
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        try:
            parsed = urlparse(url)
            if not all([parsed.scheme, parsed.netloc]):
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} URL invalide : format incorrect")
                return None
                
            # Test de connexion
            response = requests.get(url, timeout=10, headers=headers, allow_redirects=True)
            response.raise_for_status()
            
            return response.url  # Retourne l'URL finale après redirections
            
        except requests.exceptions.RequestException as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Erreur de connexion : {str(e)}")
            return None
    
    def WebsiteFoundUrl(url):
        website_url = validate_url(url)
        if website_url:
            print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Website: {white}{website_url}{red}")
        return website_url

    def WebsiteDomain(website_url):
        try:
            domain = urlparse(website_url).netloc
            print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Domain: {white}{domain}{red}")
            return domain
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Erreur lors de l'extraction du domaine : {str(e)}")
            return None

    def WebsiteIp(domain):
        if not domain:
            return None
        try:
            ip = socket.gethostbyname(domain)
            print(f"{BEFORE + current_time_hour() + AFTER} {ADD} IP: {white}{ip}{red}")
            return ip
        except socket.gaierror as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Erreur DNS : {str(e)}")
            return None

    def IpType(ip):
        if not ip:
            return
        if ':' in ip:
            type = "ipv6" 
        elif '.' in ip:
            type = "ipv4"
        else:
            return
        print(f"{BEFORE + current_time_hour() + AFTER} {ADD} IP Type: {white}{type}{red}")

    def WebsiteSecure(website_url):
        if not website_url:
            return
        print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Secure: {white}{website_url.startswith('https://')}{red}")

    def WebsiteStatus(website_url):
        if not website_url:
            return
        try:
            response = requests.get(website_url, timeout=5, headers=headers, allow_redirects=True)
            status_code = response.status_code
            if response.history:
                redirects = ' -> '.join(str(r.status_code) for r in response.history)
                print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Redirections: {white}{redirects}{red}")
        except RequestException as e:
            status_code = f"Error: {str(e)}"
        print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Status Code: {white}{status_code}{red}")

    def IpInfo(ip):
        if not ip:
            return
        try:
            api = requests.get(f"https://ipinfo.io/{ip}/json", headers=headers, timeout=5).json()
            for key in ['country', 'region', 'city', 'loc', 'timezone', 'hostname', 'org', 'asn']:
                if key in api:
                    print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Host {key.capitalize()}: {white}{api[key]}{red}")
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Erreur lors de la récupération des informations IP : {str(e)}")

    def IpDns(ip):
        if not ip:
            return
        try:
            dns = socket.gethostbyaddr(ip)[0]
            print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Host DNS: {white}{dns}{red}")
            
            # Récupération des enregistrements DNS
            domain = dns.split('.')[-2:]
            domain = '.'.join(domain)
            
            for record_type in ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA']:
                try:
                    answers = dns.resolver.resolve(domain, record_type)
                    records = [str(rdata) for rdata in answers]
                    print(f"{BEFORE + current_time_hour() + AFTER} {ADD} DNS {record_type} Records: {white}{', '.join(records)}{red}")
                except Exception:
                    pass
                    
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Erreur DNS : {str(e)}")

    def WebsitePort(ip):
        if not ip:
            return
            
        ports = [21, 22, 23, 25, 53, 69, 80, 110, 123, 143, 194, 389, 443, 161, 3306, 5432, 6379, 1521, 3389,
                 8080, 8443, 9000, 9090, 27017, 6379, 11211, 5601, 9200, 9300]  # Ajout de ports supplémentaires
                 
        port_protocol_map = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 69: "TFTP",
            80: "HTTP", 110: "POP3", 123: "NTP", 143: "IMAP", 194: "IRC", 389: "LDAP",
            443: "HTTPS", 161: "SNMP", 3306: "MySQL", 5432: "PostgreSQL", 6379: "Redis",
            1521: "Oracle DB", 3389: "RDP", 8080: "HTTP-Alt", 8443: "HTTPS-Alt",
            9000: "Portainer", 9090: "Prometheus", 27017: "MongoDB", 6379: "Redis",
            11211: "Memcached", 5601: "Kibana", 9200: "Elasticsearch", 9300: "Elasticsearch-Cluster"
        }

        def ScanPort(ip, port):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(1)
                    if sock.connect_ex((ip, port)) == 0:
                        service_info = ""
                        try:
                            if port in [80, 443, 8080, 8443]:
                                # Tentative de bannière HTTP
                                protocol = "https" if port in [443, 8443] else "http"
                                response = requests.get(f"{protocol}://{ip}:{port}", timeout=2, verify=False)
                                server = response.headers.get('Server', '')
                                if server:
                                    service_info = f" - Server: {server}"
                        except:
                            pass
                        print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Port: {white}{port}{red} Status: {white}Open{red} Protocol: {white}{port_protocol_map.get(port, 'Unknown')}{service_info}{red}")
            except:
                pass

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(lambda p: ScanPort(ip, p), ports)

    def HttpHeaders(website_url):
        if not website_url:
            return
        try:
            response = requests.get(website_url, timeout=5, verify=False)
            headers = response.headers
            security_headers = {
                'Strict-Transport-Security': 'HSTS',
                'Content-Security-Policy': 'CSP',
                'X-Frame-Options': 'Clickjacking Protection',
                'X-Content-Type-Options': 'MIME-Sniffing Protection',
                'X-XSS-Protection': 'XSS Protection',
                'Referrer-Policy': 'Referrer Policy',
                'Feature-Policy': 'Feature Policy',
                'Permissions-Policy': 'Permissions Policy'
            }
            
            for header, value in headers.items():
                security_info = f" ({security_headers[header]})" if header in security_headers else ""
                print(f"{BEFORE + current_time_hour() + AFTER} {ADD} HTTP Header: {white}{header}{security_info}{red} Value: {white}{value}{red}")
                
            # Vérification des en-têtes de sécurité manquants
            for header, description in security_headers.items():
                if header not in headers:
                    print(f"{BEFORE + current_time_hour() + AFTER} {WARNING} Missing Security Header: {white}{header}{red} ({description})")
                    
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Erreur lors de la récupération des en-têtes : {str(e)}")

    def CheckSslCertificate(website_url):
        if not website_url or not website_url.startswith('https://'):
            return
        try:
            hostname = urlparse(website_url).hostname
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Informations importantes du certificat
                    print(f"{BEFORE + current_time_hour() + AFTER} {ADD} SSL Subject: {white}{dict(x[0] for x in cert['subject'])}{red}")
                    print(f"{BEFORE + current_time_hour() + AFTER} {ADD} SSL Issuer: {white}{dict(x[0] for x in cert['issuer'])}{red}")
                    print(f"{BEFORE + current_time_hour() + AFTER} {ADD} SSL Version: {white}{cert.get('version', 'Unknown')}{red}")
                    print(f"{BEFORE + current_time_hour() + AFTER} {ADD} SSL Serial Number: {white}{cert.get('serialNumber', 'Unknown')}{red}")
                    
                    # Dates de validité
                    not_before = cert['notBefore']
                    not_after = cert['notAfter']
                    print(f"{BEFORE + current_time_hour() + AFTER} {ADD} SSL Valid From: {white}{not_before}{red}")
                    print(f"{BEFORE + current_time_hour() + AFTER} {ADD} SSL Valid Until: {white}{not_after}{red}")
                    
                    # Alternative names
                    if 'subjectAltName' in cert:
                        alt_names = [x[1] for x in cert['subjectAltName'] if x[0].lower() == 'dns']
                        print(f"{BEFORE + current_time_hour() + AFTER} {ADD} SSL Alternative Names: {white}{', '.join(alt_names)}{red}")
                    
        except ssl.SSLError as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Erreur SSL : {str(e)}")
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Erreur lors de la vérification du certificat : {str(e)}")

    def CheckSecurityHeaders(website_url):
        if not website_url:
            return
        try:
            response = requests.get(website_url, timeout=5, verify=False)
            headers = response.headers
            
            security_headers = {
                'Content-Security-Policy': {
                    'description': 'Protection contre les attaques XSS et autres injections',
                    'recommended': "default-src 'self'"
                },
                'Strict-Transport-Security': {
                    'description': 'Force HTTPS',
                    'recommended': 'max-age=31536000; includeSubDomains'
                },
                'X-Content-Type-Options': {
                    'description': 'Prévention du MIME-sniffing',
                    'recommended': 'nosniff'
                },
                'X-Frame-Options': {
                    'description': 'Protection contre le clickjacking',
                    'recommended': 'SAMEORIGIN'
                },
                'X-XSS-Protection': {
                    'description': 'Protection XSS des anciens navigateurs',
                    'recommended': '1; mode=block'
                },
                'Referrer-Policy': {
                    'description': 'Contrôle des informations de référence',
                    'recommended': 'strict-origin-when-cross-origin'
                },
                'Permissions-Policy': {
                    'description': 'Contrôle des fonctionnalités du navigateur',
                    'recommended': 'Present'
                }
            }
            
            for header, info in security_headers.items():
                if header in headers:
                    value = headers[header]
                    status = "✓" if value == info['recommended'] else "!"
                    print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Security Header: {white}{header}{red} Status: {white}{status}{red} Value: {white}{value}{red}")
                else:
                    print(f"{BEFORE + current_time_hour() + AFTER} {WARNING} Missing Security Header: {white}{header}{red} ({info['description']})")
                    
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Erreur lors de la vérification des en-têtes de sécurité : {str(e)}")

    def AnalyzeCookies(website_url):
        if not website_url:
            return
        try:
            response = requests.get(website_url, timeout=5, verify=False)
            cookies = response.cookies
            
            if not cookies:
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Aucun cookie trouvé")
                return
                
            for cookie in cookies:
                secure = 'Secure' if cookie.secure else 'Not Secure'
                httponly = 'HttpOnly' if cookie.has_nonstandard_attr('HttpOnly') else 'Not HttpOnly'
                samesite = cookie.get_nonstandard_attr('SameSite', 'Not Set')
                
                print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Cookie: {white}{cookie.name}{red}")
                print(f"   Domain: {white}{cookie.domain}{red}")
                print(f"   Path: {white}{cookie.path}{red}")
                print(f"   Secure: {white}{secure}{red}")
                print(f"   HttpOnly: {white}{httponly}{red}")
                print(f"   SameSite: {white}{samesite}{red}")
                print(f"   Expires: {white}{cookie.expires}{red}")
                
                # Analyse de sécurité
                warnings = []
                if not cookie.secure:
                    warnings.append("Cookie non sécurisé (pas d'attribut Secure)")
                if not cookie.has_nonstandard_attr('HttpOnly'):
                    warnings.append("Cookie accessible via JavaScript (pas d'attribut HttpOnly)")
                if not cookie.get_nonstandard_attr('SameSite'):
                    warnings.append("Pas de protection SameSite")
                    
                if warnings:
                    print(f"   {WARNING} Avertissements de sécurité:")
                    for warning in warnings:
                        print(f"   - {white}{warning}{red}")
                        
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Erreur lors de l'analyse des cookies : {str(e)}")

    def DetectTechnologies(website_url):
        if not website_url:
            return
        try:
            response = requests.get(website_url, timeout=5, verify=False)
            headers = response.headers
            html = response.text
            soup = BeautifulSoup(response.content, 'html.parser')
            
            technologies = {
                'Server': headers.get('Server', 'Unknown'),
                'Technologies': []
            }
            
            # En-têtes courants
            if 'x-powered-by' in headers:
                technologies['Technologies'].append(f"Powered by: {headers['x-powered-by']}")
                
            # Détection des frameworks et bibliothèques JavaScript
            js_libs = {
                'jQuery': ['jquery'],
                'React': ['react', 'reactjs'],
                'Vue.js': ['vue'],
                'Angular': ['ng-', 'angular'],
                'Bootstrap': ['bootstrap'],
                'Tailwind': ['tailwind'],
                'Next.js': ['__NEXT_DATA__'],
                'Nuxt.js': ['nuxt'],
                'Laravel': ['laravel'],
                'WordPress': ['wp-content'],
                'Drupal': ['drupal'],
                'Joomla': ['joomla'],
                'Font Awesome': ['font-awesome'],
                'Google Analytics': ['ga.js', 'analytics.js', 'gtag'],
                'Cloudflare': ['cloudflare']
            }
            
            # Recherche dans les scripts
            for script in soup.find_all('script', src=True):
                src = script['src'].lower()
                for lib, patterns in js_libs.items():
                    if any(pattern in src for pattern in patterns):
                        technologies['Technologies'].append(lib)
                        
            # Recherche dans le HTML
            for lib, patterns in js_libs.items():
                if any(pattern in html.lower() for pattern in patterns):
                    if lib not in technologies['Technologies']:
                        technologies['Technologies'].append(lib)
                        
            # Meta tags
            meta_generator = soup.find('meta', attrs={'name': 'generator'})
            if meta_generator and meta_generator.get('content'):
                technologies['Technologies'].append(f"Generator: {meta_generator['content']}")
                
            # Recherche de CMS courants
            cms_patterns = {
                'WordPress': ['/wp-content/', '/wp-includes/', 'wp-'],
                'Drupal': ['/sites/default/', 'drupal.js'],
                'Joomla': ['/templates/', 'joomla'],
                'Magento': ['/skin/frontend/', 'magento'],
                'Shopify': ['shopify', '/cdn.shopify.com/'],
                'PrestaShop': ['prestashop', '/modules/']
            }
            
            for cms, patterns in cms_patterns.items():
                if any(pattern in html for pattern in patterns):
                    technologies['Technologies'].append(f"CMS: {cms}")
                    
            # Affichage des résultats
            print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Server: {white}{technologies['Server']}{red}")
            if technologies['Technologies']:
                print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Detected Technologies:")
                for tech in set(technologies['Technologies']):  # Utilisation de set pour éviter les doublons
                    print(f"   - {white}{tech}{red}")
            else:
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} No specific technologies detected")
                
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Erreur lors de la détection des technologies : {str(e)}")

    Slow(scan_banner)
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Selected User-Agent: {white + user_agent}")
    url = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Website URL -> {reset}")
    Censored(url)
    print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Scanning..{reset}")

    website_url = WebsiteFoundUrl(url)
    if website_url:
        domain = WebsiteDomain(website_url)
        ip = WebsiteIp(domain)
        IpType(ip)
        WebsiteSecure(website_url)
        WebsiteStatus(website_url)
        IpInfo(ip)
        IpDns(ip)
        WebsitePort(ip)
        HttpHeaders(website_url)
        CheckSslCertificate(website_url)
        CheckSecurityHeaders(website_url)
        AnalyzeCookies(website_url)
        DetectTechnologies(website_url)
    Continue()
    Reset()

except Exception as e:
    Error(e)
