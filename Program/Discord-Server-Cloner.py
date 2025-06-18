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

Title("Discord Server Cloner")

# Diagnostiquer les problèmes potentiels
print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Diagnostic des dépendances pour Discord Server Cloner...")

try:
    # Vérifier si les modules requis sont disponibles
    required_modules = {
        "discord": "Module principal pour l'API Discord",
        "asyncio": "Module de gestion asynchrone",
        "requests": "Module pour les requêtes HTTP",
        "pyperclip": "Module pour copier dans le presse-papiers"
    }
    
    missing_modules = []
    for module_name, description in required_modules.items():
        try:
            module = __import__(module_name)
            if module_name == "discord":
                print(f"{BEFORE + current_time_hour() + AFTER} {SUCCESS} Module {module_name} trouvé (version: {module.__version__})")
            else:
                print(f"{BEFORE + current_time_hour() + AFTER} {SUCCESS} Module {module_name} trouvé")
        except ImportError:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Module {module_name} manquant ({description})")
            missing_modules.append(module_name)
        except AttributeError:
            print(f"{BEFORE + current_time_hour() + AFTER} {WARNING} Module {module_name} trouvé mais sans version détectée")
    
    if missing_modules:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Des modules requis sont manquants. Veuillez exécuter:")
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} python -m pip install {' '.join(missing_modules)}")
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Ou lancez 'python fix_discord_cloner.py' à la racine.")
        Continue()
        Reset()
    
    # Diagnostic spécifique pour discord.py
    if 'discord' in sys.modules:
        discord_module = sys.modules['discord']
        # Vérifier si les intents sont disponibles (discord.py 2.0+)
        if hasattr(discord_module, 'Intents'):
            print(f"{BEFORE + current_time_hour() + AFTER} {SUCCESS} Discord Intents disponibles (discord.py 2.0+)")
            intents = discord_module.Intents.default()
            if hasattr(intents, 'message_content'):
                print(f"{BEFORE + current_time_hour() + AFTER} {SUCCESS} L'intent 'message_content' est disponible")
            else:
                print(f"{BEFORE + current_time_hour() + AFTER} {WARNING} L'intent 'message_content' n'est pas disponible")
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {WARNING} Discord Intents non disponibles (discord.py < 2.0)")
    
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Démarrage du Discord Server Cloner...")
    
    # Continuer avec le code original
    import discord
    import asyncio
    import json
    import os
    import requests
    import pyperclip
    from colorama import Fore, Style, init
    import sys
    import time
    
    # Fonctions d'affichage
    def print_add(message):
        print(f'{BEFORE + current_time_hour() + AFTER} {SUCCESS} {message}')

    def print_delete(message):
        print(f'{BEFORE + current_time_hour() + AFTER} {ERROR} {message}')

    def print_warning(message):
        print(f'{BEFORE + current_time_hour() + AFTER} {WARNING} {message}')

    def print_error(message):
        print(f'{BEFORE + current_time_hour() + AFTER} {ERROR} {message}')
    
    # Classe Clone (adaptée de Prime-Cloner)
    class Clone:
        @staticmethod
        async def roles_delete(guild_to: discord.Guild):
            for role in guild_to.roles:
                try:
                    if role.name != "@everyone":
                        await role.delete()
                        print_delete(f"Deleted Role: {role.name}")
                except discord.Forbidden:
                    print_error(f"Error While Deleting Role: {role.name}")
                except discord.HTTPException:
                    print_error(f"Unable to Delete Role: {role.name}")

        @staticmethod
        async def roles_create(guild_to: discord.Guild, guild_from: discord.Guild):
            roles = []
            role: discord.Role
            for role in guild_from.roles:
                if role.name != "@everyone":
                    roles.append(role)
            roles = roles[::-1]
            for role in roles:
                try:
                    await guild_to.create_role(
                        name=role.name,
                        permissions=role.permissions,
                        colour=role.colour,
                        hoist=role.hoist,
                        mentionable=role.mentionable
                    )
                    print_add(f"Created Role {role.name}")
                except discord.Forbidden:
                    print_error(f"Error While Creating Role: {role.name}")
                except discord.HTTPException:
                    print_error(f"Unable to Create Role: {role.name}")

        @staticmethod
        async def channels_delete(guild_to: discord.Guild):
            for channel in guild_to.channels:
                try:
                    await channel.delete()
                    print_delete(f"Deleted Channel: {channel.name}")
                except discord.Forbidden:
                    print_error(f"Error While Deleting Channel: {channel.name}")
                except discord.HTTPException:
                    print_error(f"Unable To Delete Channel: {channel.name}")

        @staticmethod
        async def categories_create(guild_to: discord.Guild, guild_from: discord.Guild):
            channels = guild_from.categories
            channel: discord.CategoryChannel
            new_channel: discord.CategoryChannel
            for channel in channels:
                try:
                    overwrites_to = {}
                    for key, value in channel.overwrites.items():
                        role = discord.utils.get(guild_to.roles, name=key.name)
                        overwrites_to[role] = value
                    new_channel = await guild_to.create_category(
                        name=channel.name,
                        overwrites=overwrites_to)
                    await new_channel.edit(position=channel.position)
                    print_add(f"Created Category: {channel.name}")
                except discord.Forbidden:
                    print_error(f"Error While Creating Category: {channel.name}")
                except discord.HTTPException:
                    print_error(f"Unable To Create Category: {channel.name}")

        @staticmethod
        async def channels_create(guild_to: discord.Guild, guild_from: discord.Guild):
            channel_text: discord.TextChannel
            channel_voice: discord.VoiceChannel
            category = None
            for channel_text in guild_from.text_channels:
                try:
                    for category in guild_to.categories:
                        try:
                            if category.name == channel_text.category.name:
                                break
                        except AttributeError:
                            print_warning(f"Channel {channel_text.name} doesn't have any category!")
                            category = None
                            break

                    overwrites_to = {}
                    for key, value in channel_text.overwrites.items():
                        role = discord.utils.get(guild_to.roles, name=key.name)
                        overwrites_to[role] = value
                    try:
                        new_channel = await guild_to.create_text_channel(
                            name=channel_text.name,
                            overwrites=overwrites_to,
                            position=channel_text.position,
                            topic=channel_text.topic,
                            slowmode_delay=channel_text.slowmode_delay,
                            nsfw=channel_text.nsfw)
                    except:
                        new_channel = await guild_to.create_text_channel(
                            name=channel_text.name,
                            overwrites=overwrites_to,
                            position=channel_text.position)
                    if category is not None:
                        await new_channel.edit(category=category)
                    print_add(f"Created Text Channel: {channel_text.name}")
                except discord.Forbidden:
                    print_error(f"Error While Creating Text Channel: {channel_text.name}")
                except discord.HTTPException:
                    print_error(f"Unable To Creating Text Channel: {channel_text.name}")
                except:
                    print_error(f"Error While Creating Text Channel: {channel_text.name}")

            category = None
            for channel_voice in guild_from.voice_channels:
                try:
                    for category in guild_to.categories:
                        try:
                            if category.name == channel_voice.category.name:
                                break
                        except AttributeError:
                            print_warning(f"Channel {channel_voice.name} doesn't have any category!")
                            category = None
                            break

                    overwrites_to = {}
                    for key, value in channel_voice.overwrites.items():
                        role = discord.utils.get(guild_to.roles, name=key.name)
                        overwrites_to[role] = value
                    try:
                        new_channel = await guild_to.create_voice_channel(
                            name=channel_voice.name,
                            overwrites=overwrites_to,
                            position=channel_voice.position,
                            bitrate=channel_voice.bitrate,
                            user_limit=channel_voice.user_limit,
                            )
                    except:
                        new_channel = await guild_to.create_voice_channel(
                            name=channel_voice.name,
                            overwrites=overwrites_to,
                            position=channel_voice.position)
                    if category is not None:
                        await new_channel.edit(category=category)
                    print_add(f"Created Voice Channel: {channel_voice.name}")
                except discord.Forbidden:
                    print_error(f"Error While Creating Voice Channel: {channel_voice.name}")
                except discord.HTTPException:
                    print_error(f"Unable To Creating Voice Channel: {channel_voice.name}")
                except:
                    print_error(f"Error While Creating Voice Channel: {channel_voice.name}")

        @staticmethod
        async def emojis_delete(guild_to: discord.Guild):
            for emoji in guild_to.emojis:
                try:
                    await emoji.delete()
                    print_delete(f"Deleted Emoji: {emoji.name}")
                except discord.Forbidden:
                    print_error(f"Error While Deleting Emoji{emoji.name}")
                except discord.HTTPException:
                    print_error(f"Error While Deleting Emoji {emoji.name}")

        @staticmethod
        async def emojis_create(guild_to: discord.Guild, guild_from: discord.Guild):
            emoji: discord.Emoji
            for emoji in guild_from.emojis:
                try:
                    # Pour discord.py 2.x
                    try:
                        emoji_image = await emoji.url.read()
                    # Pour discord.py 1.x
                    except AttributeError:
                        emoji_image = await emoji.url_as(format='png').read()
                    
                    await guild_to.create_custom_emoji(
                        name=emoji.name,
                        image=emoji_image)
                    print_add(f"Created Emoji {emoji.name}")
                except discord.Forbidden:
                    print_error(f"Error While Creating Emoji {emoji.name} ")
                except discord.HTTPException:
                    print_error(f"Error While Creating Emoji {emoji.name}")

        @staticmethod
        async def guild_edit(guild_to: discord.Guild, guild_from: discord.Guild):
            try:
                try:
                    # Pour discord.py 2.x
                    try:
                        if guild_from.icon:
                            icon_bytes = await guild_from.icon.read()
                        else:
                            icon_bytes = None
                    # Pour discord.py 1.x
                    except AttributeError:
                        if guild_from.icon_url:
                            icon_bytes = await guild_from.icon_url_as(format='png').read()
                        else:
                            icon_bytes = None
                    
                    await guild_to.edit(
                        name=guild_from.name,
                        icon=icon_bytes
                    )
                    print_add(f"Server name and icon changed")
                except:
                    await guild_to.edit(
                        name=guild_from.name
                    )
                    print_add(f"Server name changed")
                    print_error(f"Error while changing server icon")
            except discord.Forbidden:
                print_error(f"Error while changing server icon and name")
            except discord.HTTPException:
                print_error(f"Error while changing server icon and name")
            
        @staticmethod
        async def guild_template(guild_to: discord.Guild):
            try:
                template = await guild_to.create_template(name="Your.Tool Server Template")
                template_url = f"https://discord.new/{template.code}"
                print_add(f"Template created: {template_url}")
                pyperclip.copy(template_url)
                print_add("Template URL copied to clipboard")
            except Exception as e:
                print_error(f"Error creating template: {e}")
    
    # Vérifier le token Discord
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Enter your Discord token")
    token = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Token -> {reset}")
    
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    r = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
    
    if r.status_code == 200:
        userName = r.json()['username'] 
        if 'discriminator' in r.json() and r.json()['discriminator'] != '0':
            userName += '#' + r.json()['discriminator']
        userID = r.json()['id']
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Logged in as: {white}{userName} ({userID}){red}")
    else:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid token")
        Continue()
        Reset()
    
    # Informations pour le clonage
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Enter the source server ID (to copy from)")
    source_guild_id = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Source server ID -> {reset}")
    
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Enter the destination server ID (to copy to)")
    dest_guild_id = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Destination server ID -> {reset}")
    
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Create a template after cloning? (y/n)")
    create_template = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} -> {reset}").lower() == 'y'
    
    # Fonction principale pour le clonage
    async def main():
        # Détecter la version de discord.py pour ajuster les intents
        try:
            discord_version = discord.__version__
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Detected discord.py version: {discord_version}")
            
            # Pour discord.py 2.x
            if int(discord_version.split('.')[0]) >= 2:
                intents = discord.Intents.default()
                intents.message_content = True
                client = discord.Client(intents=intents)
            # Pour discord.py 1.x
            else:
                client = discord.Client()
        except:
            # Fallback en cas d'erreur
            client = discord.Client()
        
        @client.event
        async def on_ready():
            print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Connected as {white}{client.user}{red}")
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Starting server cloning process...")
            
            guild_from = client.get_guild(int(source_guild_id))
            guild_to = client.get_guild(int(dest_guild_id))
            
            if not guild_from:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Source server not found")
                await client.close()
                return
                
            if not guild_to:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Destination server not found")
                await client.close()
                return
            
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Copying from '{white}{guild_from.name}{red}' to '{white}{guild_to.name}{red}'")
            
            try:
                await Clone.roles_delete(guild_to)
                await Clone.channels_delete(guild_to)
                await Clone.roles_create(guild_to, guild_from)
                await Clone.categories_create(guild_to, guild_from)
                await Clone.channels_create(guild_to, guild_from)
                await Clone.guild_edit(guild_to, guild_from)
                
                if create_template:
                    await Clone.guild_template(guild_to)
                
                print(f"\n{BEFORE + current_time_hour() + AFTER} {SUCCESS} Server cloning completed successfully!")
            except Exception as e:
                print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} An error occurred during cloning: {white}{e}")
            
            await client.close()
        
        try:
            # Pour éviter le blocage du terminal
            await client.start(token, bot=False)
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error connecting to Discord: {white}{e}")
    
    # Exécuter le clonage
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Starting cloning process...")
    
    try:
        # Exécuter le clonage de manière asynchrone
        if sys.platform.startswith('win'):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except Exception as e:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Critical error: {white}{e}")
    
    # Nettoyer le buffer et fermer proprement
    sys.stdout.flush()
    time.sleep(0.5)
    
    Continue()
    Reset()
except Exception as e:
    Error(e) 