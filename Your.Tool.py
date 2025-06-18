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
from Program.Config.LaunchState import LaunchState

try:
   import webbrowser
   import re
   import pyzipper
   from tkinter import messagebox
except Exception as e:
   ErrorModule(e)

option_01 = "Website-Vulnerability-Scanner"
option_02 = "Website-Info-Scanner"
option_03 = "Website-Url-Scanner"
option_04 = "Ip-Scanner"
option_05 = "Ip-Port-Scanner"
option_06 = "Ip-Pinger"
option_07 = "URL-Checker"
option_08 = "Get-Your-Ip"
option_09 = "Soon"
option_10 = "Soon"

option_11 = "Dox-Create"
option_12 = "Dox-Tracker"
option_13 = "Get-Image-Exif"
option_14 = "Google-Dorking"
option_15 = "Username-Tracker"
option_16 = "Email-Tracker"
option_17 = "Email-Lookup"
option_18 = "Phone-Number-Lookup"
option_19 = "Ip-Lookup"
option_20 = "Metadata"

option_21 = "Phishing-Attack"
option_22 = "Password-Zip-Cracked-Attack"
option_23 = "Password-Hash-Decrypted-Attack"
option_24 = "Password-Hash-Encrypted"
option_25 = "Search-In-DataBase"
option_26 = "Dark-Web-Links"
option_27 = "Ip-Generator"
option_28 = "Password-Generator"
option_29 = "Password-Generator-Random"
option_30 = "Password-Checker"

option_31 = "Virus-Builder"
option_32 = "RAT-Builder"
option_33 = "Spoofer"
option_34 = "Obfuscator"
option_35 = "Soon"
option_36 = "Soon"
option_37 = "Soon"
option_38 = "Soon"
option_39 = "Soon"
option_40 = "Soon"

option_41 = "Roblox-Cookie-Login"
option_42 = "Roblox-Cookie-Info"
option_43 = "Roblox-Id-Info"
option_44 = "Roblox-User-Info"
option_45 = "Soon"
option_46 = "Soon"
option_47 = "Soon"
option_48 = "Soon"
option_49 = "Soon"
option_50 = "Soon"

option_51 = "Discord-Token-Nuker"
option_52 = "Discord-Token-Info"
option_53 = "Discord-Token-Joiner"
option_54 = "Discord-Token-Leaver"
option_55 = "Discord-Token-Login"
option_56 = "Discord-Token-To-Id-And-Brute"
option_57 = "Discord-Token-Server-Raid"
option_58 = "Discord-Token-Spammer"
option_59 = "Discord-Token-Delete-Friends"
option_60 = "Discord-Token-Block-Friends"
option_61 = "Discord-Token-Mass-Dm"
option_62 = "Discord-Token-Delete-Dm"
option_63 = "Discord-Token-Status-Changer"
option_64 = "Discord-Token-Language-Changer"
option_65 = "Discord-Token-House-Changer"
option_66 = "Discord-Token-Theme-Changer"
option_67 = "Discord-Token-Generator"
option_68 = "Discord-Bot-Server-Nuker"
option_69 = "Discord-Bot-Invite-To-Id"
option_70 = "Discord-Server-Info"
option_71 = "Discord-Nitro-Generator"
option_72 = "Discord-Webhook-Info"
option_73 = "Discord-Webhook-Delete"
option_74 = "Discord-Webhook-Spammer"
option_75 = "Discord-Webhook-Generator"
option_76 = "Discord-Bot-Server-Backup"
option_77 = "Discord-Id-to-Token-First-Part"
option_78 = "Discord-Grab-Analyze"
option_79 = "Discord-Server-Cloner"

option_80 = "File-Encryptor"
option_81 = "File-Decryptor"
option_82 = "File-Converter"
option_83 = "File-Scanner"
option_84 = "Steganography"
option_85 = "Archive-Cracker"
option_86 = "SMB-Cracker"
option_87 = "Winrar-Premium"
option_88 = "Soon"
option_89 = "Soon"

option_90 = "Facebook-Downloader"
option_91 = "Youtube-Downloader"
option_92 = "TikTok-Downloader"
option_93 = "Site-Downloader"
option_94 = "TikTok-Views"
option_95 = "Soon"
option_96 = "Soon"
option_97 = "Soon"
option_98 = "Soon"
option_99 = "Soon"

option_next = "Next"
option_back = "Back"
option_site = "Site"
option_info = "Info"

option_01_txt = f"{green}[{white}01{green}]{white} " + option_01.ljust(30)[:30].replace("-", " ")
option_02_txt = f"{green}[{white}02{green}]{white} " + option_02.ljust(30)[:30].replace("-", " ")
option_03_txt = f"{green}[{white}03{green}]{white} " + option_03.ljust(30)[:30].replace("-", " ")
option_04_txt = f"{green}[{white}04{green}]{white} " + option_04.ljust(30)[:30].replace("-", " ")
option_05_txt = f"{green}[{white}05{green}]{white} " + option_05.ljust(30)[:30].replace("-", " ")
option_06_txt = f"{green}[{white}06{green}]{white} " + option_06.ljust(30)[:30].replace("-", " ")
option_07_txt = f"{green}[{white}07{green}]{white} " + option_07.ljust(30)[:30].replace("-", " ")
option_08_txt = f"{green}[{white}08{green}]{white} " + option_08.ljust(30)[:30].replace("-", " ")
option_09_txt = f"{green}[{white}09{green}]{white} " + option_09.ljust(30)[:30].replace("-", " ")
option_10_txt = f"{green}[{white}10{green}]{white} " + option_10.ljust(30)[:30].replace("-", " ")

option_11_txt = f"{green}[{white}11{green}]{white} " + option_11.ljust(30)[:30].replace("-", " ")
option_12_txt = f"{green}[{white}12{green}]{white} " + option_12.ljust(30)[:30].replace("-", " ")
option_13_txt = f"{green}[{white}13{green}]{white} " + option_13.ljust(30)[:30].replace("-", " ")
option_14_txt = f"{green}[{white}14{green}]{white} " + option_14.ljust(30)[:30].replace("-", " ")
option_15_txt = f"{green}[{white}15{green}]{white} " + option_15.ljust(30)[:30].replace("-", " ")
option_16_txt = f"{green}[{white}16{green}]{white} " + option_16.ljust(30)[:30].replace("-", " ")
option_17_txt = f"{green}[{white}17{green}]{white} " + option_17.ljust(30)[:30].replace("-", " ")
option_18_txt = f"{green}[{white}18{green}]{white} " + option_18.ljust(30)[:30].replace("-", " ")
option_19_txt = f"{green}[{white}19{green}]{white} " + option_19.ljust(30)[:30].replace("-", " ")
option_20_txt = f"{green}[{white}20{green}]{white} " + option_20.ljust(30)[:30].replace("-", " ")

option_21_txt = f"{green}[{white}21{green}]{white} " + option_21.ljust(30)[:30].replace("-", " ")
option_22_txt = f"{green}[{white}22{green}]{white} " + option_22.ljust(30)[:30].replace("-", " ")
option_23_txt = f"{green}[{white}23{green}]{white} " + option_23.ljust(30)[:30].replace("-", " ")
option_24_txt = f"{green}[{white}24{green}]{white} " + option_24.ljust(30)[:30].replace("-", " ")
option_25_txt = f"{green}[{white}25{green}]{white} " + option_25.ljust(30)[:30].replace("-", " ")
option_26_txt = f"{green}[{white}26{green}]{white} " + option_26.ljust(30)[:30].replace("-", " ")
option_27_txt = f"{green}[{white}27{green}]{white} " + option_27.ljust(30)[:30].replace("-", " ")
option_28_txt = f"{green}[{white}28{green}]{white} " + option_28.ljust(30)[:30].replace("-", " ")
option_29_txt = f"{green}[{white}29{green}]{white} " + option_29.ljust(30)[:30].replace("-", " ")
option_30_txt = f"{green}[{white}30{green}]{white} " + option_30.ljust(30)[:30].replace("-", " ")

option_31_txt = f"{green}[{white}31{green}]{white} " + option_31.ljust(30)[:30].replace("-", " ")
option_32_txt = f"{green}[{white}32{green}]{white} " + option_32.ljust(30)[:30].replace("-", " ")
option_33_txt = f"{green}[{white}33{green}]{white} " + option_33.ljust(30)[:30].replace("-", " ")
option_34_txt = f"{green}[{white}34{green}]{white} " + option_34.ljust(30)[:30].replace("-", " ")
option_35_txt = f"{green}[{white}35{green}]{white} " + option_35.ljust(30)[:30].replace("-", " ")
option_36_txt = f"{green}[{white}36{green}]{white} " + option_36.ljust(30)[:30].replace("-", " ")
option_37_txt = f"{green}[{white}37{green}]{white} " + option_37.ljust(30)[:30].replace("-", " ")
option_38_txt = f"{green}[{white}38{green}]{white} " + option_38.ljust(30)[:30].replace("-", " ")
option_39_txt = f"{green}[{white}39{green}]{white} " + option_39.ljust(30)[:30].replace("-", " ")
option_40_txt = f"{green}[{white}40{green}]{white} " + option_40.ljust(30)[:30].replace("-", " ")

option_41_txt = f"{green}[{white}41{green}]{white} " + option_41.ljust(30)[:30].replace("-", " ")
option_42_txt = f"{green}[{white}42{green}]{white} " + option_42.ljust(30)[:30].replace("-", " ")
option_43_txt = f"{green}[{white}43{green}]{white} " + option_43.ljust(30)[:30].replace("-", " ")
option_44_txt = f"{green}[{white}44{green}]{white} " + option_44.ljust(30)[:30].replace("-", " ")
option_45_txt = f"{green}[{white}45{green}]{white} " + option_45.ljust(30)[:30].replace("-", " ")
option_46_txt = f"{green}[{white}46{green}]{white} " + option_46.ljust(30)[:30].replace("-", " ")
option_47_txt = f"{green}[{white}47{green}]{white} " + option_47.ljust(30)[:30].replace("-", " ")
option_48_txt = f"{green}[{white}48{green}]{white} " + option_48.ljust(30)[:30].replace("-", " ")
option_49_txt = f"{green}[{white}49{green}]{white} " + option_49.ljust(30)[:30].replace("-", " ")
option_50_txt = f"{green}[{white}50{green}]{white} " + option_50.ljust(30)[:30].replace("-", " ")

option_51_txt = f"{green}[{white}51{green}]{white} " + option_51.ljust(30)[:30].replace("-", " ")
option_52_txt = f"{green}[{white}52{green}]{white} " + option_52.ljust(30)[:30].replace("-", " ")
option_53_txt = f"{green}[{white}53{green}]{white} " + option_53.ljust(30)[:30].replace("-", " ")
option_54_txt = f"{green}[{white}54{green}]{white} " + option_54.ljust(30)[:30].replace("-", " ")
option_55_txt = f"{green}[{white}55{green}]{white} " + option_55.ljust(30)[:30].replace("-", " ")
option_56_txt = f"{green}[{white}56{green}]{white} " + option_56.ljust(30)[:30].replace("-", " ")
option_57_txt = f"{green}[{white}57{green}]{white} " + option_57.ljust(30)[:30].replace("-", " ")
option_58_txt = f"{green}[{white}58{green}]{white} " + option_58.ljust(30)[:30].replace("-", " ")
option_59_txt = f"{green}[{white}59{green}]{white} " + option_59.ljust(30)[:30].replace("-", " ")
option_60_txt = f"{green}[{white}60{green}]{white} " + option_60.ljust(30)[:30].replace("-", " ")

option_61_txt = f"{green}[{white}61{green}]{white} " + option_61.ljust(30)[:30].replace("-", " ")
option_62_txt = f"{green}[{white}62{green}]{white} " + option_62.ljust(30)[:30].replace("-", " ")
option_63_txt = f"{green}[{white}63{green}]{white} " + option_63.ljust(30)[:30].replace("-", " ")
option_64_txt = f"{green}[{white}64{green}]{white} " + option_64.ljust(30)[:30].replace("-", " ")
option_65_txt = f"{green}[{white}65{green}]{white} " + option_65.ljust(30)[:30].replace("-", " ")
option_66_txt = f"{green}[{white}66{green}]{white} " + option_66.ljust(30)[:30].replace("-", " ")
option_67_txt = f"{green}[{white}67{green}]{white} " + option_67.ljust(30)[:30].replace("-", " ")
option_68_txt = f"{green}[{white}68{green}]{white} " + option_68.ljust(30)[:30].replace("-", " ")
option_69_txt = f"{green}[{white}69{green}]{white} " + option_69.ljust(30)[:30].replace("-", " ")
option_70_txt = f"{green}[{white}70{green}]{white} " + option_70.ljust(30)[:30].replace("-", " ")

option_71_txt = f"{green}[{white}71{green}]{white} " + option_71.ljust(30)[:30].replace("-", " ")
option_72_txt = f"{green}[{white}72{green}]{white} " + option_72.ljust(30)[:30].replace("-", " ")
option_73_txt = f"{green}[{white}73{green}]{white} " + option_73.ljust(30)[:30].replace("-", " ")
option_74_txt = f"{green}[{white}74{green}]{white} " + option_74.ljust(30)[:30].replace("-", " ")
option_75_txt = f"{green}[{white}75{green}]{white} " + option_75.ljust(30)[:30].replace("-", " ")
option_76_txt = f"{green}[{white}76{green}]{white} " + option_76.ljust(30)[:30].replace("-", " ")
option_77_txt = f"{green}[{white}77{green}]{white} " + option_77.ljust(30)[:30].replace("-", " ")
option_78_txt = f"{green}[{white}78{green}]{white} " + option_78.ljust(30)[:30].replace("-", " ")
option_79_txt = f"{green}[{white}79{green}]{white} " + option_79.ljust(30)[:30].replace("-", " ")

option_80_txt = f"{green}[{white}80{green}]{white} " + option_80.ljust(30)[:30].replace("-", " ")
option_81_txt = f"{green}[{white}81{green}]{white} " + option_81.ljust(30)[:30].replace("-", " ")
option_82_txt = f"{green}[{white}82{green}]{white} " + option_82.ljust(30)[:30].replace("-", " ")
option_83_txt = f"{green}[{white}83{green}]{white} " + option_83.ljust(30)[:30].replace("-", " ")
option_84_txt = f"{green}[{white}84{green}]{white} " + option_84.ljust(30)[:30].replace("-", " ")
option_85_txt = f"{green}[{white}85{green}]{white} " + option_85.ljust(30)[:30].replace("-", " ")
option_86_txt = f"{green}[{white}86{green}]{white} " + option_86.ljust(30)[:30].replace("-", " ")
option_87_txt = f"{green}[{white}87{green}]{white} " + option_87.ljust(30)[:30].replace("-", " ")
option_88_txt = f"{green}[{white}88{green}]{white} " + option_88.ljust(30)[:30].replace("-", " ")
option_89_txt = f"{green}[{white}89{green}]{white} " + option_89.ljust(30)[:30].replace("-", " ")
option_90_txt = f"{green}[{white}90{green}]{white} " + option_90.ljust(30)[:30].replace("-", " ")
option_91_txt = f"{green}[{white}91{green}]{white} " + option_91.ljust(30)[:30].replace("-", " ")
option_92_txt = f"{green}[{white}92{green}]{white} " + option_92.ljust(30)[:30].replace("-", " ")
option_93_txt = f"{green}[{white}93{green}]{white} " + option_93.ljust(30)[:30].replace("-", " ")
option_94_txt = f"{green}[{white}94{green}]{white} " + option_94.ljust(30)[:30].replace("-", " ")
option_95_txt = f"{green}[{white}95{green}]{white} " + option_95.ljust(30)[:30].replace("-", " ")
option_96_txt = f"{green}[{white}96{green}]{white} " + option_96.ljust(30)[:30].replace("-", " ")
option_97_txt = f"{green}[{white}97{green}]{white} " + option_97.ljust(30)[:30].replace("-", " ")
option_98_txt = f"{green}[{white}98{green}]{white} " + option_98.ljust(30)[:30].replace("-", " ")
option_99_txt = f"{green}[{white}99{green}]{white} " + option_99.ljust(30)[:30].replace("-", " ")

option_back_txt = option_back + f" {green}[{white}B{green}]{white}"
option_next_txt = option_next + f" {green}[{white}N{green}]{white}"
option_site_txt = f"{green}[{white}S{green}]{white} " + option_site
option_info_txt =  f"{green}[{white}I{green}]{white} " + option_info

menu1 = f""" {green}┌─ {option_info_txt}                                                                                               {option_next_txt} {green}─┐
 ├─ {option_site_txt} {green}┌─────────────────┐                        ┌───────┐                           ┌───────────┐            │
 └─┬─────────┤ {white}Network Scanner{green} ├─────────┬──────────────┤ {white}Osint{green} ├──────────────┬────────────┤ {white}Utilities{green} ├────────────┴─
   {green}│{green}         └─────────────────┘         {green}│{green}              └───────┘              {green}│{green}            └───────────┘
   ├{green}─{white} {option_01_txt                    }{green}├{green}─{white} {option_11_txt                    }{green}├{green}─{white} {option_21_txt}
   ├{green}─{white} {option_02_txt                    }{green}├{green}─{white} {option_12_txt                    }{green}├{green}─{white} {option_22_txt}
   ├{green}─{white} {option_03_txt                    }{green}├{green}─{white} {option_13_txt                    }{green}├{green}─{white} {option_23_txt}
   ├{green}─{white} {option_04_txt                    }{green}├{green}─{white} {option_14_txt                    }{green}├{green}─{white} {option_24_txt}
   ├{green}─{white} {option_05_txt                    }{green}├{green}─{white} {option_15_txt                    }{green}├{green}─{white} {option_25_txt}
   ├{green}─{white} {option_06_txt                    }{green}├{green}─{white} {option_16_txt                    }{green}├{green}─{white} {option_26_txt}
   ├{green}─{white} {option_07_txt                    }{green}├{green}─{white} {option_17_txt                    }{green}├{green}─{white} {option_27_txt}
   └{green}─{white} {option_08_txt                    }{green}├{green}─{white} {option_18_txt                    }{green}├{green}─{white} {option_28_txt}
                                         {green}├{green}─{white} {option_19_txt                    }{green}├{green}─{white} {option_29_txt}
                                         {green}└{green}─{white} {option_20_txt                    }{green}└{green}─{white} {option_30_txt}{green}
"""

menu2 = f""" {green}┌─ {option_info_txt}                                                                                                {option_next_txt} {green}─┐
 ├─ {option_site_txt}  {green}┌───────────────┐                         ┌──────┐                              ┌────────┐    {white}{option_back_txt} {green}─┤
─┴─┬──────────┤ {white}Virus Builder{green} ├──────────┬──────────────┤ {white}Tool{green} ├───────────────┬──────────────┤ {white}Roblox{green} ├──────────────┴─
   {green}│{green}          └───────────────┘          {green}│{green}              └──────┘               {green}│{green}              └────────┘
   └{green}─{white} {option_31_txt                    }{green}├{green}─{white} {option_32_txt                    }{green}├{green}─{white} {option_41_txt}
           {green}├{green}─{white} Stealer                    {green}├{green}─{white} {option_33_txt                    }{green}├{green}─{white} {option_42_txt}
           {green}│{green}  ├{green}─{white} System Info             {green}├{green}─{white} {option_34_txt                    }{green}├{green}─{white} {option_43_txt}
           {green}│{green}  ├{green}─{white} Discord Token/Injection {green}├{green}─{white} {option_35_txt                    }{green}├{green}─{white} {option_44_txt}
           {green}│{green}  ├{green}─{white} Browser Steal           {green}├{green}─{white} {option_36_txt                    }{green}└{green}─{white} {option_45_txt}
           {green}│{green}  ├{green}─{white} Roblox Cookie           {green}└{green}─{white} {option_37_txt                    }
           {green}│{green}  └{green}─{white} Other                            
           {green}└{green}─{white} Malware                    
              {green}├{green}─{white} Anti VM & Debug                                             
              {green}├{green}─{white} Startup                                                    
              {green}└{green}─{white} Other{green}                          
"""

menu3 = f""" {green}┌─ {option_info_txt}                                                                                                {option_next_txt} {green}─┐
 ├─ {option_site_txt}                                           {green}┌─────────┐                                          {white}{option_back_txt} {green}─┤
─┴─┬─────────────────────────────────────┬─────────────┤ {white}Discord{green} ├─────────────┬──────────────────────────────────────┴─
   {green}│{green}                                     {green}│{green}             └─────────┘             {green}│{green}          
   ├{green}─{white} {option_51_txt                    }{green}├{green}─{white} {option_61_txt                    }{green}├{green}─{white} {option_71_txt}
   ├{green}─{white} {option_52_txt                    }{green}├{green}─{white} {option_62_txt                    }{green}├{green}─{white} {option_72_txt}
   ├{green}─{white} {option_53_txt                    }{green}├{green}─{white} {option_63_txt                    }{green}├{green}─{white} {option_73_txt}
   ├{green}─{white} {option_54_txt                    }{green}├{green}─{white} {option_64_txt                    }{green}├{green}─{white} {option_74_txt}
   ├{green}─{white} {option_55_txt                    }{green}├{green}─{white} {option_65_txt                    }{green}├{green}─{white} {option_75_txt}
   ├{green}─{white} {option_56_txt                    }{green}├{green}─{white} {option_66_txt                    }{green}├{green}─{white} {option_76_txt}
   ├{green}─{white} {option_57_txt                    }{green}├{green}─{white} {option_67_txt                    }{green}├{green}─{white} {option_77_txt}
   ├{green}─{white} {option_58_txt                    }{green}├{green}─{white} {option_68_txt                    }{green}├{green}─{white} {option_78_txt}
   ├{green}─{white} {option_59_txt                    }{green}├{green}─{white} {option_69_txt                    }{green}└{green}─{white} {option_79_txt}
   └{green}─{white} {option_60_txt                    }{green}└{green}─{white} {option_70_txt                    }{green}
"""

menu4 = f""" {green}┌─ {option_info_txt}                                                                                               {option_next_txt} ─┐
 ├─ {option_site_txt}{green}┌────────────┐                          ┌──────────┐                        ┌─────────────┐    {white}{option_back_txt} {green}─┤
─┴─┬────────┤ {white}File Tools{green} ├────────────┬─────────────┤ {white}Crackers{green} ├────────────┬───────────┤ {white}Downloaders{green} ├──────────────┴─
   {green}│{green}        └────────────┘            {green}│{green}             └──────────┘            {green}│{green}           └─────────────┘
   ├{green}─{white} {option_80_txt                  }{green}├{green}─{white} {option_85_txt                    }{green}├{green}─{white} {option_90_txt                    }
   ├{green}─{white} {option_81_txt                  }{green}├{green}─{white} {option_86_txt                    }{green}├{green}─{white} {option_91_txt                    }
   ├{green}─{white} {option_82_txt                  }{green}├{green}─{white} {option_87_txt                    }{green}├{green}─{white} {option_92_txt                    }
   ├{green}─{white} {option_83_txt                  }{green}├{green}─{white} {option_88_txt                    }{green}├{green}─{white} {option_93_txt                    }
   └{green}─{white} {option_84_txt                  }{green}└{green}─{white} {option_89_txt                    }{green}└{green}─{white} {option_94_txt                    }{green}
"""

# Initialisation de l'état de lancement
launch_state = LaunchState(tool_path)

def Update():
   popup_version = ""
   try:
      new_version = re.search(r'version_tool\s*=\s*"([^"]+)"', requests.get(url_config).text).group(1)
      if new_version != version_tool:
         webbrowser.open(f"https://{github_tool}")
         colorama.init()
         input(f"{BEFORE + current_time_hour() + AFTER} {INFO} Please install the new version of the tool: {white + version_tool + red} -> {white + new_version} ")
         popup_version = f"{red}New Version: {white + version_tool + red} -> {white + new_version}"
         colorama.deinit()
         Clear()
   except: pass
   
   # Redirection vers votre site uniquement au premier lancement
   if launch_state.is_first_launch():
      try:
         webbrowser.open(f"https://www.josh-studio.com")
         launch_state.set_launched()  # Marquer comme déjà lancé
      except: pass

   return popup_version

menu_path = os.path.join(tool_path, "Program", "Config", "Menu.txt")

def Menu():
   popup_version = Update()

   try:
      with open(menu_path, "r") as file:
         menu_number = file.read()
      menu_mapping = {"1": menu1, "2": menu2, "3": menu3, "4": menu4}
      menu = menu_mapping.get(menu_number, menu1)
   except:
      menu = menu1
      menu_number = "1"

   title_ascii_art = f"""
                   ██╗   ██╗ ██████╗ ██╗   ██╗██████╗            ████████╗ ██████╗  ██████╗ ██╗     
                   ╚██╗ ██╔╝██╔═══██╗██║   ██║██╔══██╗           ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
                    ╚████╔╝ ██║   ██║██║   ██║██████╔╝              ██║   ██║   ██║██║   ██║██║     
                     ╚██╔╝  ██║   ██║██║   ██║██╔══██╗              ██║   ██║   ██║██║   ██║██║     
                      ██║   ╚██████╔╝╚██████╔╝██║  ██║    ██╗       ██║   ╚██████╔╝╚██████╔╝███████╗
                      ╚═╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝    ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝"""

   banner = f"""{popup_version}                                                                                      
{MainColor2(title_ascii_art)}{white}

                                           {green}{github_tool}{white}
{menu}"""
   return banner, menu_number

while True:
   try:
      Clear()

      banner, menu_number = Menu()

      Title(f"Menu {menu_number}")
      Slow(MainColor(banner))

      choice = input(MainColor(f""" 

 {green}┌──({white}{username_pc}@your.tool{green})─{green}[{white}~/{os_name}/Menu-{menu_number}{green}]
 └─{white}$ {reset}"""))

      if choice in ['N', 'n', 'NEXT', 'Next', 'next']:
            menu_number = {"1": "2", "2": "3", "3": "4", "4": "1"}.get(menu_number, "1")
            with open(menu_path, "w") as file:
               file.write(menu_number)
            continue

      elif choice in ['B', 'b', 'BACK', 'Back', 'back']:
            menu_number = {"2": "1", "3": "2", "4": "3"}.get(menu_number, "1")
            with open(menu_path, "w") as file:
               file.write(menu_number)
            continue

      elif choice in ['I', 'i', 'INFO', 'Info', 'info']:
            StartProgram(f"{option_info}.py")
            continue

      elif choice in ['S', 's', 'SITE', 'Site', 'site']:
            StartProgram(f"{option_site}.py")
            continue
      
      elif choice == '31':
         print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Pour le Virus Builder, je vous recommande fortement d'utiliser celui de RedTiger qui est le plus complet et le plus stable.")
         print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Je vous redirige vers le projet RedTiger-Tools...")
         
         try:
            webbrowser.open("https://github.com/loxy0dev/RedTiger-Tools")
            print(f"\n{BEFORE + current_time_hour() + AFTER} {SUCCESS} Redirection effectuée avec succès !")
         except:
            print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Impossible d'ouvrir le lien automatiquement.")
            print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Voici le lien à copier dans votre navigateur : https://github.com/loxy0dev/RedTiger-Tools")

      elif choice == '33':
         StartProgram("Spoofer.py")
         Continue()
         
      options = {
         '01': option_01, '02': option_02, '03': option_03, '04': option_04,
         '05': option_05, '06': option_06, '07': option_07, '08': option_08,
         '09': option_09, '10': option_10, '11': option_11, '12': option_12,
         '13': option_13, '14': option_14, '15': option_15, '16': option_16,
         '17': option_17, '18': option_18, '19': option_19, '20': option_20,
         '21': option_21, '22': option_22, '23': option_23, '24': option_24,
         '25': option_25, '26': option_26, '27': option_27, '28': option_28,
         '29': option_29, '30': option_30, '31': option_31, '32': option_32,
         '33': option_33, '34': option_34, '35': option_35, '36': option_36,
         '37': option_37, '38': option_38, '39': option_39, '40': option_40,
         '41': option_41, '42': option_42, '43': option_43, '44': option_44,
         '45': option_45, '46': option_46, '47': option_47, '48': option_48,
         '49': option_49, '50': option_50, '51': option_51, '52': option_52,
         '53': option_53, '54': option_54, '55': option_55, '56': option_56,
         '57': option_57, '58': option_58, '59': option_59, '60': option_60,
         '61': option_61, '62': option_62, '63': option_63, '64': option_64,
         '65': option_65, '66': option_66, '67': option_67, '68': option_68,
         '69': option_69, '70': option_70, '71': option_71, '72': option_72,
         '73': option_73, '74': option_74, '75': option_75, '76': option_76,
         '77': option_77, '78': option_78, '79': option_79, '80': option_80,
         '81': option_81, '82': option_82, '83': option_83, '84': option_84,
         '85': option_85, '86': option_86, '87': option_87, '88': option_88,
         '89': option_89, '90': option_90, '91': option_91, '92': option_92,
         '93': option_93, '94': option_94, '95': option_95, '96': option_96,
         '97': option_97, '98': option_98, '99': option_99
      }

      if choice in options:  
         StartProgram(f"{options[choice]}.py")
      elif '0' + choice in options:
         StartProgram(f"{options['0' + choice]}.py")
      else:
         ErrorChoiceStart()

   except Exception as e:
      Error(e)
