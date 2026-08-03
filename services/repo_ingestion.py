from sqlalchemy.orm import Session

from models.repository import Repository
from crud.repository import read_repo_with_github_url, create_repo
from .github.url_validation import validate_and_parse_github_url
from .github.client import get_repository, check_public, make_RepositoryCreate_Obj

from .file_processing.discover_file_paths import get_all_repo_files
from .file_processing.file_filtering import filter_supported_file_paths
from .file_processing.read_file import get_text_content
from schemas.file import FileCreate
from crud.file import create_file, read_file_with_path_and_repo_id
from pathlib import Path

from .github.archive import download_and_extract_repo
from tempfile import TemporaryDirectory #to get temporary directory created by python

from .file_processing.chunking.create_chunk import create_chunks
from .chunk_service import create_chunks_with_embeddings

"""
validate user's passed in github URL
using githug api, get repo's response dictionary get_repository(...)
create a RepositoryCreate Pydantic model 
insert that into "repositories" table 

download the repo files
then call helper_ingest_files
"""
def ingest_repository(db : Session, github_url : str)-> Repository | None: 

    #validate and parse 
    owner, repo_name, normalized_url = validate_and_parse_github_url(github_url=github_url)

    #invalid URL
    if not owner or not repo_name:  
        return None

    #see if the repo already exists or not, in the repositories table
    repo = read_repo_with_github_url(db, github_url=normalized_url)

    #repo already exist
    if repo:
        return None 
    
    #else, get_repository as json() -> dict
    repo_response_dict = get_repository(owner=owner, repo_name=repo_name)

    #check if (not a public repo)
    if not repo_response_dict or not check_public(repo_response_dict=repo_response_dict):
        return None
    
    #create a RepositoryCreate object ready to insert to the db
    repo_create_pydantic_obj = make_RepositoryCreate_Obj(owner=owner, repo_name=repo_name, repo_response_dict=repo_response_dict)

     #insert that RepositoryCreate object using curd's create_repo into the database
    repository_obj = create_repo(db, repo_data=repo_create_pydantic_obj)

    #download the repo
    with TemporaryDirectory() as temp_directory: 
        repo_root = download_and_extract_repo(
            owner=repo_create_pydantic_obj.owner, 
            repo_name=repo_create_pydantic_obj.name, 
            commit_sha=repo_create_pydantic_obj.latest_commit_sha, 
            temp_directory=Path(temp_directory))

        #call ingest_files here (access the files while temp_directory still exists)
        helper_ingest_files(db=db, repo_root=repo_root, repository_obj=repository_obj)

    return repository_obj


"""
loop thru the repo_root directory
    get the list of all file paths 
    get the list of only the supported file paths

for each file path 
    read the file - get the text_content
    create a FileCreate Pydantic Object 
    insert into Files table

    chunk the file
        get list of all chunks with no embeddings (this call create_chunks that chunk each file with ast module or tree sitter)
        create embeddings of the chunks and 
        insert those chunks into Chunks table 
"""
def helper_ingest_files(db : Session, repo_root : Path, repository_obj : Repository) -> None:
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

        #creates the file_path to make it a relative path -> represents the file's location inside the repository (w/o the temp_directory path)
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

        #chunk here 

        #get list[ChunkRawWithNoEmbeddings]
        list_chunkRawWithNoEmbeddings = create_chunks(
            text_content=text_content, 
            relative_file_path_str=file_path_str,
            file_id=file_obj.id
            )

        #if create_chunks is not created, skip
        if not list_chunkRawWithNoEmbeddings:
            continue

        #TODO later, not commit in create_file but use flush so that a file with no chunks won't exist in the Files table

        #create embeddings of those chunks 
        #insert the Chunks to the databate
        create_chunks_with_embeddings(
            db=db, 
            chunk_datas_with_no_embeddings=list_chunkRawWithNoEmbeddings)
       

