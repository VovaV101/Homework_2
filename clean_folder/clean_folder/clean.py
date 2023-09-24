import re
import sys
from pathlib import Path
import shutil
from transliterate import translit

CATEGORIES = {"Audio" : [".mp3", ".wav", ".ogg", ".amr"],
            "Docs" : [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"],
            "Images": [".jpeg", ".png", ".jpg", ".svg"],
            "Video" : [".avi", ".mp4", ".mov", ".mkv"],
            "Archives" : [".zip", ".gz", ".tar"]}
def normalize(text):
    transliterated_text = translit(text, 'uk', reversed=True)
    normalized_text = re.sub(r'[^a-zA-Z0-9]', '_', transliterated_text)
    normalized_text = normalized_text.lower()
    return normalized_text

def get_categories(file:Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"
  
def move_file(file: Path, category: str, root_dir: Path) -> None:
    target_dir = root_dir.joinpath(category)
    if not target_dir.exists():
        target_dir.mkdir()
    new_filename = normalize(file.stem) + file.suffix
    new_path = target_dir.joinpath(new_filename)
    if not new_path.exists():
        file.replace(new_path)

def remove_empty_folders(root_dir):
    root_path = Path(root_dir)
    for folder_path in root_path.iterdir():
        if folder_path.is_dir():
            remove_empty_folders(folder_path)
            if not list(folder_path.iterdir()):
                folder_path.rmdir()

def extract_and_move_archives(root_dir):
    root_path = Path(root_dir)
    archive_dir = root_path / "Archives"

    for archive_path in root_path.glob("**/*.*"):
        try:
            archive_name = archive_path.stem
            archive_subdir = archive_dir / archive_name
            if not archive_subdir.exists():
                archive_subdir.mkdir()
            shutil.unpack_archive(archive_path, archive_subdir)
            archive_path.unlink()
        except shutil.ReadError:
            pass

def sort_folder(path:Path) -> None:
    for element in path.glob("**/*"):
        if element.is_file():
            category = get_categories(element)
            move_file(element, category, path)
    
    
def main() -> str:
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return 'No path to folder'  

    if not path.exists():
        return "Folder does not exists"
    
    sort_folder(path)
    extract_and_move_archives(path)
    remove_empty_folders(path)

    return "All ok"
        

if __name__ == '__main__':
    main()
