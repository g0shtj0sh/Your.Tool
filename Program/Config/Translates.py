# Copyright (c) Your.Tool (https://www.josh-studio.com)
# See the file 'LICENSE' for copying permission
# ----------------------------------------------------------------------------------------------------------------------------------------------------------|
# EN: 
#     - Do not touch or modify the code below. If there is an error, please contact the owner, but under no circumstances should you touch the code.
#     - Do not resell this tool, do not credit it to yours.
# FR: 
#     - Ne pas toucher ni modifier le code ci-dessous. En cas d'erreur, veuillez contacter le propriétaire, mais en aucun cas vous ne devez toucher au code.
#     - Ne revendez pas ce tool, ne le créditez pas au vôtre.

from .Config import language_tool
from .Util import color, white, green, reset, red, blue, yellow

# Variable LANGUAGE utilisée par tous les modules
LANGUAGE = language_tool

# Variables de couleur
primary = green
secondary = white

# Dictionnaire de traductions pour les différentes langues
translations = {
    "EN": {
        # Traductions générales
        "Choice": "Choose an option",
        "Chose": "Choose an option",
        "Error": "Error",
        "File": "File",
        "NotExist": "does not exist",
        "ProgramStop": "Program stopped",
        "CancelOp": "Operation cancelled",
        "ErrorURL": "Invalid URL. Please enter a valid URL starting with http:// or https://",
        
        # Site-Downloader.py
        "Website_url": "Enter the website URL to download",
        "1SiteDownload": "Website",
        "2SiteDownload": "has been downloaded to",
        "ErrorDownloadSite": "Error downloading the site:",
        
        # Steganography.py
        "MessageEncode": "Message encoded successfully in",
        "EncodeMessage": "Encode a message in an image",
        "DecodeMessage": "Decode a message from an image",
        "PathImage": "Enter the path to the image",
        "ImageNotExist": "Image does not exist",
        "MessageToEncode": "Enter the message to encode",
        "PathEncodedImage": "Enter the path to the encoded image",
        "DecodedMessage": "Decoded message",
        
        # SMB-Cracker.py
        "ATTEMPT": "ATTEMPT",
        "PasswdFound": "Password found:",
        "PasswdNoFound": "Password not found",
        "EnterIPAdress": "Enter the IP address",
        "EnterUsername": "Enter the username",
        "EnterPassList": "Enter the password list path",
        
        # RAT-Builder.py
        "TokenBot": "Enter your Discord bot token",
        "ChannelIDRAT": "Enter the channel ID for the RAT",
        "FileName": "Enter the output file name",
        "RatSucces": "RAT has been successfully generated at",
        "ObfY": "Do you want to obfuscate the RAT? (y/n)",
        "ObfSucces": "RAT has been successfully obfuscated at",
        
        # Password-Generator.py
        "ThreadsNumber": "Enter the number of threads",
        "FileSizeReached": "Maximum file size reached",
        
        # Password-Checker.py
        "PassEvaluate": "Enter the password to evaluate",
        "PassStrength": "Password strength",
        "TimeCrackPass": "Estimated time to crack",
        
        # Metadata.py
        "Metadatafor": "Metadata for",
        "Metadata": "Metadata",
        "SuccesUpdate": "successfully updated to",
        "ErrorMetadata": "Error updating metadata:",
        "ViewMetadata": "View metadata",
        "EditMetadata": "Edit metadata",
        "FilePath": "Enter the file path",
        "FiealdModify": "Enter the field to modify",
        "NewValue": "Enter the new value for",
        
        # Get-Your-Ip.py
        "IpSearch": "Searching for IP information...",
        "PCHostname": "PC Hostname",
        "PCUsername": "PC Username",
        "PCDisplayName": "PC Display Name",
        "IpPublic": "Public IP",
        "Iplocal": "Local IP",
        "Ipv6": "IPv6",
        
        # File-Encryptor.py
        "CryptMethod": "Choose encryption method",
        "PathFileEncrypt": "Enter the path of the file to encrypt",
        "PasswdCrypt": "Enter the encryption password",
        "ErrorReadFile": "Error reading file",
        "SaveFileEncrypt": "Encrypted file saved to",
        "ErrorEncryptFile": "Error encrypting file:",
        
        # File-Decryptor.py
        "DecryptFile": "Decrypt a file",
        "PathToDecrypt": "Enter the path of the file to decrypt",
        "PasswdForDecrypt": "Enter the decryption password",
        "DecryptedContent": "Decrypted content saved to",
        "ErrorDecrypt": "Error decrypting file:",
        
        # File-Converter.py
        "ConvertionNotSupport": "Conversion not supported",
        "ConvertOptions": "Conversion options",
        "FileConvertedSucces": "File successfully converted to",
        
        # Facebook-Downloader.py
        "DownloadDone": "Download completed",
        "URLVideo": "Enter the video URL",
        
        # Winrar-Premium.py
        "LaunchAdmin": "Launching with administrator privileges...",
        "WinPremium": "Do you want to activate WinRAR premium? (y/n)",
        "WinActive": "WinRAR has been successfully activated",
        "ErrorWinActive": "Error activating WinRAR:",
        
        # URL-Checker.py
        "Error_file_not_found": "File not found",
        "URL_to_check": "Enter the URL to check",
        "Malicious_URL": "engines detected this URL as malicious",
        "No_found_for_url": "No information found for this URL"
    },
    "FR": {
        # Traductions générales
        "Choice": "Choisissez une option",
        "Chose": "Choisissez une option",
        "Error": "Erreur",
        "File": "Fichier",
        "NotExist": "n'existe pas",
        "ProgramStop": "Programme arrêté",
        "CancelOp": "Opération annulée",
        "ErrorURL": "URL invalide. Veuillez entrer une URL valide commençant par http:// ou https://",
        
        # Site-Downloader.py
        "Website_url": "Entrez l'URL du site Web à télécharger",
        "1SiteDownload": "Le site Web",
        "2SiteDownload": "a été téléchargé dans",
        "ErrorDownloadSite": "Erreur lors du téléchargement du site:",
        
        # Steganography.py
        "MessageEncode": "Message encodé avec succès dans",
        "EncodeMessage": "Encoder un message dans une image",
        "DecodeMessage": "Décoder un message à partir d'une image",
        "PathImage": "Entrez le chemin de l'image",
        "ImageNotExist": "L'image n'existe pas",
        "MessageToEncode": "Entrez le message à encoder",
        "PathEncodedImage": "Entrez le chemin de l'image encodée",
        "DecodedMessage": "Message décodé",
        
        # SMB-Cracker.py
        "ATTEMPT": "ESSAI",
        "PasswdFound": "Mot de passe trouvé:",
        "PasswdNoFound": "Mot de passe non trouvé",
        "EnterIPAdress": "Entrez l'adresse IP",
        "EnterUsername": "Entrez le nom d'utilisateur",
        "EnterPassList": "Entrez le chemin de la liste de mots de passe",
        
        # RAT-Builder.py
        "TokenBot": "Entrez votre token de bot Discord",
        "ChannelIDRAT": "Entrez l'ID du canal pour le RAT",
        "FileName": "Entrez le nom du fichier de sortie",
        "RatSucces": "Le RAT a été généré avec succès à",
        "ObfY": "Voulez-vous obfusquer le RAT? (y/n)",
        "ObfSucces": "Le RAT a été obfusqué avec succès à",
        
        # Password-Generator.py
        "ThreadsNumber": "Entrez le nombre de threads",
        "FileSizeReached": "Taille maximale du fichier atteinte",
        
        # Password-Checker.py
        "PassEvaluate": "Entrez le mot de passe à évaluer",
        "PassStrength": "Force du mot de passe",
        "TimeCrackPass": "Temps estimé pour cracker",
        
        # Metadata.py
        "Metadatafor": "Métadonnées pour",
        "Metadata": "Métadonnée",
        "SuccesUpdate": "mise à jour avec succès à",
        "ErrorMetadata": "Erreur lors de la mise à jour des métadonnées:",
        "ViewMetadata": "Voir les métadonnées",
        "EditMetadata": "Modifier les métadonnées",
        "FilePath": "Entrez le chemin du fichier",
        "FiealdModify": "Entrez le champ à modifier",
        "NewValue": "Entrez la nouvelle valeur pour",
        
        # Get-Your-Ip.py
        "IpSearch": "Recherche d'informations sur l'IP...",
        "PCHostname": "Nom d'hôte PC",
        "PCUsername": "Nom d'utilisateur PC",
        "PCDisplayName": "Nom d'affichage PC",
        "IpPublic": "IP publique",
        "Iplocal": "IP locale",
        "Ipv6": "IPv6",
        
        # File-Encryptor.py
        "CryptMethod": "Choisissez la méthode de chiffrement",
        "PathFileEncrypt": "Entrez le chemin du fichier à chiffrer",
        "PasswdCrypt": "Entrez le mot de passe de chiffrement",
        "ErrorReadFile": "Erreur de lecture du fichier",
        "SaveFileEncrypt": "Fichier chiffré enregistré dans",
        "ErrorEncryptFile": "Erreur lors du chiffrement du fichier:",
        
        # File-Decryptor.py
        "DecryptFile": "Déchiffrer un fichier",
        "PathToDecrypt": "Entrez le chemin du fichier à déchiffrer",
        "PasswdForDecrypt": "Entrez le mot de passe de déchiffrement",
        "DecryptedContent": "Contenu déchiffré enregistré dans",
        "ErrorDecrypt": "Erreur lors du déchiffrement du fichier:",
        
        # File-Converter.py
        "ConvertionNotSupport": "Conversion non prise en charge",
        "ConvertOptions": "Options de conversion",
        "FileConvertedSucces": "Fichier converti avec succès en",
        
        # Facebook-Downloader.py
        "DownloadDone": "Téléchargement terminé",
        "URLVideo": "Entrez l'URL de la vidéo",
        
        # Winrar-Premium.py
        "LaunchAdmin": "Lancement avec privilèges administrateur...",
        "WinPremium": "Voulez-vous activer WinRAR premium? (y/n)",
        "WinActive": "WinRAR a été activé avec succès",
        "ErrorWinActive": "Erreur lors de l'activation de WinRAR:",
        
        # URL-Checker.py
        "Error_file_not_found": "Fichier non trouvé",
        "URL_to_check": "Entrez l'URL à vérifier",
        "Malicious_URL": "moteurs ont détecté cette URL comme malveillante",
        "No_found_for_url": "Aucune information trouvée pour cette URL"
    }
} 