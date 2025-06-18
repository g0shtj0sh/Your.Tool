import os
import shutil
import zipfile
from pathlib import Path

def create_wordlists_archive():
    """Crée une archive des wordlists."""
    wordlists_dir = Path("2-Input/WorldList")
    if not wordlists_dir.exists():
        return
    
    with zipfile.ZipFile("wordlists.zip", "w", zipfile.ZIP_DEFLATED) as zf:
        for file in wordlists_dir.glob("*.zip"):
            zf.write(file, file.name)

def create_templates_archive():
    """Crée une archive des templates."""
    templates_dir = Path("Program/FileDetectedByAntivirus/Templates")
    if not templates_dir.exists():
        return
    
    with zipfile.ZipFile("templates.zip", "w", zipfile.ZIP_DEFLATED) as zf:
        for file in templates_dir.rglob("*"):
            if file.is_file():
                zf.write(file, file.relative_to(templates_dir))

def main():
    # Créer le dossier release s'il n'existe pas
    release_dir = Path("release_assets")
    release_dir.mkdir(exist_ok=True)
    
    # Créer les archives
    print("Création des archives...")
    os.chdir(str(Path(__file__).parent))
    
    create_wordlists_archive()
    create_templates_archive()
    
    # Déplacer les archives dans le dossier release
    for file in Path(".").glob("*.zip"):
        shutil.move(str(file), str(release_dir / file.name))
    
    print(f"\nArchives créées dans le dossier {release_dir}:")
    for file in release_dir.glob("*"):
        print(f"- {file.name}")

if __name__ == "__main__":
    main() 