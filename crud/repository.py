
from models.repository import Repository #SQLAlchemy model
from schemas.repository import RepositoryCreate, RepositoryUpdate #Pydantic model 

from sqlalchemy.orm import Session
from sqlalchemy import select

def create_repo(db: Session, repo_data : RepositoryCreate) -> Repository:    
    #repo_data = valided Pydantic object containing the reposiotory info 
    #-> Repository = returns SQLAlchemy Repository object 

    #create the ORM object
    new_repo = Repository(
        github_url=str(repo_data.github_url),
        name=repo_data.name,
        owner=repo_data.owner,
        default_branch=repo_data.default_branch,
        latest_commit_sha=repo_data.latest_commit_sha,
        ingestion_status=repo_data.ingestion_status
    )
    #add the object to the session
    db.add(new_repo)
    
    #save the transaction in the database
    db.commit()

    #reloads new_repo from the database (updates the Python Object with database-generated values, id, created_at, updated_at)
    db.refresh(new_repo)

    # returns the newly created SQLAlchemy object, INCLUDING generated values (by the database)
    return new_repo 


def read_repo_with_id(db : Session, repo_id : int) -> Repository | None:
    #-> Repository | None = returns the found Repository or None 

    statement = select(Repository).where( #SQLAlchemy knows to look at repositories table 
        Repository.id == repo_id
    )
    # executes the statement and extracts the mapped Repository object
    return db.scalar(statement) 


def read_repo_with_github_url(db : Session, github_url : str) -> Repository | None:
    statement = select(Repository).where(
        Repository.github_url == github_url
    )
    return db.scalar(statement)


def update_repo(db : Session, repo : Repository, repo_data : RepositoryUpdate) -> Repository:
    
    # convert the Pydantic repo_data RepositoryCreate model into a Dict***
    update_data = repo_data.model_dump(exclude_unset=True) # includes only the fields the user has provided 

    if "github_url" in update_data: 
        update_data["github_url"] = str(update_data["github_url"])

    for field, value in update_data.items(): #loop thru the dict
        setattr(repo, field, value) #same as repo.field = value, syntax = setattr(object, attribute_name, value)

    db.commit()
    db.refresh(repo)

    return repo #returns the updated repo with updated fields


def delete_repo_with_id(db : Session, repo_id : int) -> bool: 

    #for simple look up with PRIMARY KEY, use this, instead of select()
    repo = db.get(Repository, repo_id)

    if repo is None:
        return False
    
    db.delete(repo)
    db.commit()

    return True 