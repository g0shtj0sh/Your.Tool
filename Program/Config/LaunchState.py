# Copyright (c) Your.Tool (https://www.josh-studio.com)
# See the file 'LICENSE' for copying permission
# ----------------------------------------------------------------------------------------------------------------------------------------------------------|
# EN: 
#     - Do not touch or modify the code below. If there is an error, please contact the owner, but under no circumstances should you touch the code.
#     - Do not resell this tool, do not credit it to yours.
# FR: 
#     - Ne pas toucher ni modifier le code ci-dessous. En cas d'erreur, veuillez contacter le propriétaire, mais en aucun cas vous ne devez toucher au code.
#     - Ne revendez pas ce tool, ne le créditez pas au vôtre.

import os

class LaunchState:
    def __init__(self, tool_path):
        self.state_file = os.path.join(tool_path, "Program", "Config", "launch_state.txt")
        
    def is_first_launch(self):
        # Si le fichier n'existe pas, c'est le premier lancement
        if not os.path.exists(self.state_file):
            return True
        
        # Lire l'état depuis le fichier
        with open(self.state_file, 'r') as f:
            state = f.read().strip()
            return state == "True"
    
    def set_launched(self):
        # Marquer comme déjà lancé
        with open(self.state_file, 'w') as f:
            f.write("False") 