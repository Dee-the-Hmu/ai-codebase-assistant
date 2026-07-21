"""

ingest_repository(get the github_url )
    validate it and extract owner and repo name  using url_validation
    confrim it is a public repo (call GitHub API) using client.py's get_repository, check_public
        get repo's metadata and default branch and latest commit sha for that branch
        get RepositoryCreate Pydantic Model 
    create Repository record (using the above RepositoryCreate model)
        check for existing repository 
    Calls curd's repository_create 
    continue ingestion
        download repo (ZIP/TAR archive using the commit SHA)
        extract into a temporary directory

Use the downloaded files (extracted repository)
    walk thru directories
    filter unsupported or ignored files 
    read supported files 

    create File records 
    chunk each File's Content
    
    build searchable texts
    create embeddings
    store Chunk records

"""

from sqlalchemy.orm import Session

from models.repository import Repository
from crud.repository import read_repo_with_github_url, create_repo
from github.url_validation import validate_and_parse_github_url
from github.client import get_repository, check_public, make_RepositoryCreate_Obj

from file_processing.discover_file_paths import get_all_repo_files
from file_processing.file_filtering import filter_supported_file_paths
from file_processing.read_file import get_text_content
from models.file import File
from schemas.file import FileCreate
from crud.file import create_file, read_file_with_path_and_repo_id
from pathlib import Path

def ingest_repository(db : Session, github_url : str)-> Repository | None: 

    #validate and parse 
    owner, repo_name, normalized_url = validate_and_parse_github_url(github_url=github_url)

    #invalid URL
    if not owner or not repo_name:  
        return None

    #see if the repo already exists or not in the repositories table
    repo = read_repo_with_github_url(db, github_url=normalized_url)

    #repo already exist
    if repo:
        return None 
    
    #else, get_repository as json() -> dict
    repo_response_dict = get_repository(owner=owner, repo_name=repo_name)

    #check if (not a public repo)
    if not check_public(repo_response_dict=repo_response_dict):
        return None
    
    #create a RepositoryCreate object ready to insert to the db
    repo_create_pydantic_obj = make_RepositoryCreate_Obj(owner=owner, repo_name=repo_name, repo_response_dict=repo_response_dict)

    #insert that RepositoryCreate object using curd's create_repo into the database
    repository_obj = create_repo(db, repo_data=repo_create_pydantic_obj)

    return repository_obj

def ingest_files(db : Session, repo_root : Path, repository_obj : Repository) -> list[Path]:
    #discover all file paths
    list_of_all_file_paths = get_all_repo_files(repo_root=repo_root)

    #filter only the supported files' paths
    list_of_all_supported_file_paths = filter_supported_file_paths(list_of_all_file_paths)

    for file_path in list_of_all_supported_file_paths: 

        #read the text_content 
        text_content = get_text_content(file_path=file_path)
        
        #skips unreadable or empty files 
        if text_content is None or not text_content.strip():
            continue #dont create the File


        #creates the file_path to make it a relative path -> to store useful relative file_paths inside the files
        relative_file_path = file_path.relative_to(repo_root)
        
        #turns it into str for database
        file_path_str = str(relative_file_path)

        #check if the file already exist in the files table 
        existing_file = read_file_with_path_and_repo_id(db, file_path=file_path_str, repo_id=repository_obj.id)

        if existing_file: #if file already inside the table, don't add it again
            continue


        #else, create a FileCreate Pydantic Object ready to insert to the db
        file_create_pydantic_obj = FileCreate(
            repo_id=repository_obj.id,
            path=file_path_str,
            name=file_path.name,
            size_bytes=file_path.stat().st_size
        )

        #insert that FileCreate object using curd's create_file into the the database
        file_obj = create_file(db, file_data=file_create_pydantic_obj)

        #chunk here (continue ingesting)
        ...

       

