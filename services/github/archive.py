"""
after ingest_repo() 
    download ZIP/TAR archive using the commit SHA
        define the url to download (zipped file)
        execute the get(url)
        write the response.content into to a temp_directory/repository.zip
        extract (unzip) that into temp_directory/extracted
        return the one top-level folder from the extracted 

        
"""
from pathlib import Path
from schemas.config import settings 
from zipfile import ZipFile #use to open .zip file, read the files inside it, extract files
 
import requests 

BASE_URL = "https://api.github.com"

HEADERS = {
    "Authorization" : f"Bearer {settings.github_token}",
    "Accept" : "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

def download_and_extract_repo(owner : str, repo_name : str, commit_sha: str, temp_directory : str) -> Path:

    #url to download 
    archive_url = f"{BASE_URL}/repos/{owner}/{repo_name}/zipball/{commit_sha}"

    #execute the get(url to download)
    response = requests.get(
        url=archive_url,
        headers=HEADERS,
        timeout=60
    )

    # get the ZIP files back 
    response.raise_for_status()

    #path to the temp_directory 
    temp_path = Path(temp_directory)
    archive_path = temp_path / "repository.zip"
    extraction_path = temp_path / "extracted" # folder where the ZIP contents are extracted

    # write the zip files into archive_path (this is downloading the ZIP file)
    archive_path.write_bytes(response.content) #response.content = the downloaded ZIP file as raw bytes

    #create the "extracted" folder 
    extraction_path.mkdir(parents=True, exist_ok=True) #if exist, don't create (to avoid raisng an error)

    # unzip
    with ZipFile(archive_path, "r") as zip_file: #opens the ZIP archive in read mode 
        zip_file.extractall(extraction_path) # extracts everything inside the ZIP into the extracted directory

    extracted_items = list(extraction_path.iterdir()) # all the items (files) inside the extracted

    #checks if the extraction directory contains EXACTLY 1 top-level item (github archives normally contain 1 root repository)
    if len(extracted_items) != 1: 
        raise ValueError("Unexpected archive structure")
    
    # gets the 1 top-level folder from the extracted archive 
    repo_root = extracted_items[0] 

    if not repo_root.is_dir():
        raise ValueError("Repository root is not a directory")

    return repo_root
