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
from Config.Translates import *

current_language = LANGUAGE

def tr(key):
    return translations[current_language].get(key, key)

try:
    import random
    import string
    import json
    import requests
    import threading
    import keyboard  
    import time
    import datetime
except Exception as e:
    ErrorModule(e)

Title("Roblox Robux Generator")

# Bannière stylisée
robux_banner = f"""
   ██████╗  ██████╗ ██████╗ ██╗   ██╗██╗  ██╗     ██████╗ ███████╗███╗   ██╗
   ██╔══██╗██╔═══██╗██╔══██╗██║   ██║╚██╗██╔╝    ██╔════╝ ██╔════╝████╗  ██║
   ██████╔╝██║   ██║██████╔╝██║   ██║ ╚███╔╝     ██║  ███╗█████╗  ██╔██╗ ██║
   ██╔══██╗██║   ██║██╔══██╗██║   ██║ ██╔██╗     ██║   ██║██╔══╝  ██║╚██╗██║
   ██║  ██║╚██████╔╝██████╔╝╚██████╔╝██╔╝ ██╗    ╚██████╔╝███████╗██║ ╚████║
   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝     ╚═════╝ ╚══════╝╚═╝  ╚═══╝
"""
Slow(MainColor2(robux_banner))

running = True  
valid_codes = []  # Liste pour stocker les codes valides

def stop_program():
    global running
    running = False
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Program stopped.")

# Remplacer le raccourci global par une méthode de vérification du focus
# keyboard.add_hotkey('esc', stop_program)  # Ajout d'un raccourci pour la touche Échap

try:
    try:
        threads_number = int(input(f"\n{INPUT} {tr('ThreadsNumber')} -> {color.RESET}"))
    except:
        ErrorNumber()

    use_webhook = input(f"\n{INPUT} {tr('SendWebhook')} (y/n) -> {color.RESET}")
    webhook_url = None
    
    if use_webhook.lower() in ['y', 'yes', 'oui', 'o']:
        webhook_url = input(f"\n{INPUT} Webhook URL -> {color.RESET}")
        
        # Test du webhook avant de commencer
        try:
            test_payload = {
                'content': f"**Test Webhook** - Roblox Robux Generator starting...",
                'username': "Your.Crack St34l3r",
                'avatar_url': 'https://github.com/g0shtj0sh.png'
            }
            
            test_headers = {
                'Content-Type': 'application/json'
            }
            
            test_response = requests.post(webhook_url, data=json.dumps(test_payload), headers=test_headers)
            
            if test_response.status_code == 204:
                print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Webhook test successful!")
            else:
                print(f"\n{BEFORE + current_time_hour() + AFTER} {WARNING} Webhook test failed with status code {test_response.status_code}")
                print(f"{BEFORE + current_time_hour() + AFTER} {WARNING} Make sure your webhook URL is correct and has permissions to send messages")
                retry = input(f"\n{INPUT} Do you want to try again with a different webhook URL? (y/n) -> {color.RESET}")
                if retry.lower() in ['y', 'yes', 'oui', 'o']:
                    webhook_url = input(f"\n{INPUT} New Webhook URL -> {color.RESET}")
                else:
                    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Continuing without webhook functionality")
                    webhook_url = None
        except Exception as e:
            print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Error testing webhook: {str(e)}")
            print(f"{BEFORE + current_time_hour() + AFTER} {WARNING} Continuing without webhook functionality")
            webhook_url = None

    def send_webhook(embed_content, is_final=False):
        if not webhook_url:
            return
            
        try:
            payload = {
                'embeds': [embed_content],
                'username': "Your.Crack St34l3r",
                'avatar_url': 'https://github.com/g0shtj0sh.png'
            }

            headers = {
                'Content-Type': 'application/json'
            }

            # Ajouter un message supplémentaire dans le rapport final
            if is_final:
                payload['content'] = f"**Generator stopped** - {len(valid_codes)} valid codes found out of {total_generated} generated"

            response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
            
            if response.status_code == 204:
                if not is_final:
                    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Code sent to webhook successfully!")
                return True
            else:
                print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Webhook error: Status code {response.status_code}")
                return False
        except Exception as e:
            print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Webhook error: {str(e)}")
            return False

    def get_timestamp():
        # Fonction pour générer un timestamp compatible avec Discord sans avertissement de dépréciation
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def robux_check():
        global valid_codes
        try:
            code_robux = ''.join([random.choice(string.ascii_uppercase + string.digits) for _ in range(10)])
            url_robux = f'https://roblox.com/gift-codes/{code_robux}'
            
            # Faire la requête avec un timeout plus long
            try:
                response = requests.get(f'https://roblox.com/api/v1/gift-codes/{code_robux}/validate', timeout=5)
                
                # Analyser la réponse
                is_valid = False
                try:
                    if response.status_code == 200:
                        data = response.json()
                        is_valid = data.get('valid', False)
                except:
                    is_valid = False
                
                if is_valid:
                    valid_codes.append(url_robux)  # Ajouter à la liste des codes valides
                    
                    if webhook_url:
                        embed_content = {
                            'title': f'Robux Valid Code Found!',
                            'description': f"**__Robux Code:__**\n```{url_robux}```",
                            'color': 0x00a805,  # Vert
                            'timestamp': get_timestamp(),
                            'footer': {
                                "text": f"{name_tool} v{version_tool}",
                                "icon_url": 'https://github.com/g0shtj0sh.png',
                            }
                        }
                        # Envoyer immédiatement au webhook
                        send_webhook(embed_content)
                    
                    print(f"{valid}[{secondary}{current_time_hour()}{valid}] {GEN_VALID} Status:  {color.WHITE}Valid{color.GREEN}  | Robux: {color.WHITE}{url_robux}{color.GREEN}{reset}")
                else:
                    print(f"{invalid}[{secondary}{current_time_hour()}{invalid}] {GEN_INVALID} Status: {color.WHITE}Invalid{color.RED} | Robux: {color.WHITE}{url_robux}{color.RED}{reset}")
            except requests.Timeout:
                print(f"{invalid}[{secondary}{current_time_hour()}{invalid}] {GEN_INVALID} Status: {color.WHITE}Timeout{color.RED} | Robux: {color.WHITE}{url_robux}{color.RED}{reset}")
            except Exception as e:
                print(f"{invalid}[{secondary}{current_time_hour()}{invalid}] {GEN_INVALID} Status: {color.WHITE}Error{color.RED} | Robux: {color.WHITE}{url_robux}{color.RED}{reset}")
        except Exception as e:
            # Continue silently on minor errors to keep the generator running
            pass

    def request():
        threads = []
        try:
            for _ in range(int(threads_number)):
                if not running:  # Vérifier si le programme doit s'arrêter
                    break
                t = threading.Thread(target=robux_check)
                t.start()
                threads.append(t)
        except:
            ErrorNumber()

        for thread in threads:
            thread.join()

    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Generating codes...")
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Press ESC to stop\n")
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} To stop the generator, press Ctrl+C in this window.")

    total_generated = 0
    start_time = time.time()
    
    try:
        while running:  
            request()
            total_generated += threads_number
            
            # Afficher les statistiques toutes les 100 générations
            if total_generated % 100 == 0:
                elapsed_time = time.time() - start_time
                rate = total_generated / elapsed_time if elapsed_time > 0 else 0
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} {tr('Generated')}: {white}{total_generated}{green} | {tr('Rate')}: {white}{rate:.2f}{green} {tr('CodesPerSecond')}")
    except KeyboardInterrupt:
        stop_program()
    
    # Rapport final
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} {tr('TotalGenerated')}: {white}{total_generated}")
    
    # Afficher les codes valides trouvés
    if len(valid_codes) > 0:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Valid codes found: {white}{len(valid_codes)}")
        for i, code in enumerate(valid_codes):
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Valid code #{i+1}: {white}{code}")
        
        # Envoyer un rapport final au webhook
        if webhook_url:
            final_embed = {
                'title': f'Robux Generator Report',
                'description': f"**Generation completed**\n\n**Total generated:** {total_generated}\n**Valid codes found:** {len(valid_codes)}",
                'color': 0x00a805,  # Vert
                'timestamp': get_timestamp(),
                'footer': {
                    "text": f"{name_tool} v{version_tool}",
                    "icon_url": 'https://github.com/g0shtj0sh.png',
                }
            }
            
            # Ajouter les codes valides au rapport
            if len(valid_codes) > 0:
                valid_codes_text = "\n".join([f"{i+1}. `{code}`" for i, code in enumerate(valid_codes)])
                final_embed['fields'] = [
                    {
                        "name": "Valid Codes",
                        "value": valid_codes_text if len(valid_codes_text) < 1024 else f"{len(valid_codes)} codes found. Too many to display.",
                        "inline": False
                    }
                ]
            
            send_webhook(final_embed, is_final=True)
    else:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} No valid codes found.")
        
        # Envoyer un rapport final au webhook même si aucun code valide n'a été trouvé
        if webhook_url:
            final_embed = {
                'title': f'Robux Generator Report',
                'description': f"**Generation completed**\n\n**Total generated:** {total_generated}\n**Valid codes found:** 0",
                'color': 0x00a805,  # Changé de orange à vert
                'timestamp': get_timestamp(),
                'footer': {
                    "text": f"{name_tool} v{version_tool}",
                    "icon_url": 'https://github.com/g0shtj0sh.png',
                }
            }
            send_webhook(final_embed, is_final=True)
    
    Continue()
    Reset()
except Exception as e:
    Error(e)

