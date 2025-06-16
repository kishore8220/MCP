from mcp.server.fastmcp import FastMCP
import os
import shutil
import hashlib
from pathlib import Path

mcp = FastMCP("FolderOrganizer")

def hash_file(filepath):
    """Returns SHA256 hash of a file (used to detect duplicates)."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

@mcp.tool()
def organize_folder(path: str = ".") -> str:
    """
    Organizes files in the given directory:
    - Groups files by type (Images, Documents, etc.)
    - Deletes exact duplicates
    - Moves files into type-based folders
    """
    if not os.path.isdir(path):
        return f"Invalid path: {path}"

    file_types = {
        "Images": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"],
        "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".csv"],
        "Videos": [".mp4", ".mov", ".avi", ".mkv"],
        "Audio": [".mp3", ".wav", ".m4a"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"]
    }

    seen_hashes = set()
    duplicates = []
    organized = 0

    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if not os.path.isfile(file_path):
            continue

        # Duplicate detection
        file_hash = hash_file(file_path)
        if file_hash in seen_hashes:
            os.remove(file_path)
            duplicates.append(file)
            continue
        seen_hashes.add(file_hash)

        ext = Path(file).suffix.lower()
        category = next((folder for folder, exts in file_types.items() if ext in exts), "Others")
        target_folder = os.path.join(path, category)
        os.makedirs(target_folder, exist_ok=True)
        shutil.move(file_path, os.path.join(target_folder, file))
        organized += 1

    return f"✅ Organized {organized} files. 🗑️ Deleted {len(duplicates)} duplicates."

if __name__ == "__main__":
    mcp.run(transport="stdio")



