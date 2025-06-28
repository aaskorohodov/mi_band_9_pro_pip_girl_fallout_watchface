import os
import re
import shutil
# noinspection PyPep8Naming
import xml.etree.ElementTree as ET
from datetime import datetime
from colorama import init, Fore

init(autoreset=True)


def find_fprj_title(fprj_path):
    tree = ET.parse(fprj_path)
    root = tree.getroot()
    screen = root.find("Screen")
    return screen.attrib.get("Title") if screen is not None else None


def safe_move_existing(filepath, output_folder):
    if os.path.exists(filepath):
        old_versions_dir = os.path.join(output_folder, "old_versions")
        os.makedirs(old_versions_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        basename = os.path.basename(filepath)
        backup_name = f"{basename}.backup_{timestamp}"
        backup_path = os.path.join(old_versions_dir, backup_name)
        print(f"{Fore.YELLOW}⚠ Existing file {basename} -> moved to {backup_path}")
        shutil.move(filepath, backup_path)


def process_face_files(root_folder):
    for dirpath, dirnames, filenames in os.walk(root_folder):
        if os.path.basename(dirpath) != "output":
            continue

        print(dirpath)

        face_files = [
            f for f in filenames
            if f.endswith(".face") and f.startswith("PipGirlProject")
        ]

        if len(face_files) != 1:
            if len(face_files) > 1:
                print(f"{Fore.RED}⛔ Skipping folder (multiple .face files): {dirpath}")
            continue

        face_file = face_files[0]
        output_path = os.path.join(dirpath, face_file)
        parent_dir = os.path.dirname(dirpath)

        # Must contain preview image
        preview_path = os.path.join(parent_dir, "preview_default_large.png")
        if not os.path.isfile(preview_path):
            continue

        # Find .fprj files in parent folder
        fprj_files = [f for f in os.listdir(parent_dir) if f.endswith(".fprj")]
        if not fprj_files:
            continue

        fprj_path = os.path.join(parent_dir, fprj_files[0])
        title = find_fprj_title(fprj_path)
        if not title:
            print(f"{Fore.RED}⚠ Failed to read title from: {fprj_path}")
            continue

        title_modified = re.sub(r'v\d+', version_override, title)
        new_face_name = f"{title_modified}.face"
        new_face_path = os.path.join(dirpath, new_face_name)

        if output_path == new_face_path:
            continue  # Already has correct name

        safe_move_existing(new_face_path, dirpath)
        print(f"{Fore.GREEN}✔ Renaming {face_file} → {new_face_name}")
        os.rename(output_path, new_face_path)


if __name__ == '__main__':

    search_here_path = 'C:/Users/DY/Downloads/Watchfaces'
    version_override = 'v9'

    process_face_files(search_here_path)
