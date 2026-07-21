"""
using the list of the paths to all files
    only include the files that we support 
"""

from pathlib import Path 

SUPPORTED_EXTENSIONS = {
    ".py",
    ".java",
    ".js",
    ".ts",
    ".html",
    ".css",
    ".sql",
    ".md",
    ".json",
    ".yaml",
    ".yml",
    ".xml",
    ".txt",
}

IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    "dist",
    "build",
    "target",
}

IGNORED_FILE_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
}

MAX_FILE_SIZE_BYTES = 1_000_000

def filter_supported_file_paths(file_paths : list[Path]) -> list[Path]:

    supported_file_paths = []

    for file_path in file_paths: 

        # for directory_name in file_path.parts: # path.parts split a Path into its individual folder and file-name components
        #     if directory_name in IGNORED_DIRECTORIES:
        #         continue
        #continue don't skip the file above 

        if any(
            directory_name in IGNORED_DIRECTORIES
            for directory_name in file_path.parts
        ):
            continue

        if file_path.name in IGNORED_FILE_NAMES: #file_path.name = only the final part of the part "e.g. filename.py"
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        if file_path.stat().st_size > MAX_FILE_SIZE_BYTES: #file size
            continue

        supported_file_paths.append(file_path)

    return supported_file_paths




        
