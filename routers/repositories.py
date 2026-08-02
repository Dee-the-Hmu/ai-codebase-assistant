from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas.repository import RepositoryResponse, RepositoryIngestRequest
from models.repository import Repository
from services.repo_ingestion import ingest_repository



router = APIRouter(prefix="/repositories", 
                   tags=["repositories"] #group these endpoints under repositories if FASTAPI auto documentation
        )

@router.post(
    "",
    response_model=RepositoryResponse, #tells FastAPI what the returned response should look like 
    status_code=status.HTTP_201_CREATED #sets the successful response status to 201
    )
def create_repository_endpoint(
    request : RepositoryIngestRequest, #frontend sends github_url as JSON
    db : Session = Depends(get_db), #tells FastAPI to call the get_db dependency and use the yielded session
    ) -> Repository:

    #validate the github repo url, download, chunk and embeds
    repo = ingest_repository(db=db, github_url=request.github_url)

    if repo is None:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Repository could not be ingested or already exists"
        )

    return repo



# @router.get("")


# @router.get("/{repo_id}")


# @router.delete("/{repo_id}")