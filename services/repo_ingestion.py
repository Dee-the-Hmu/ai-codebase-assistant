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