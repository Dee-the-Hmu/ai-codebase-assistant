"""
given a path to the repo_root (top lvl folder) of the extracted folder
    iterate the files and 
    return a list of the paths to all files
"""
from pathlib import Path 
def get_all_repo_files(repo_root : Path) -> list[Path]:

    files_paths = []

    for path in repo_root.rglob("*"): #rglob("*") = recursively finds everything inside it, including nested files and folders
        if path.is_file():
            files_paths.append(path)
        
    return files_paths
