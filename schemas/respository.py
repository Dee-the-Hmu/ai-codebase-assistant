from pydantic import BaseModel, HttpUrl, ConfigDict
from datetime import datetime


class RepositoryBase(BaseModel):
    github_url : HttpUrl
    name : str
    owner : str
    default_branch : str
    latest_commit_sha : str | None = None
    ingestion_status : str

class RepositoryUpdate(BaseModel): # each field is optional, the client can send only the fields they want to change
    github_url: HttpUrl | None = None
    name: str | None = None
    owner: str | None = None
    default_branch: str | None = None
    latest_commit_sha: str | None = None
    ingestion_status: str | None = None


class RepositoryCreate(RepositoryBase):
    pass

class RepositoryResponse(RepositoryBase):
    id : int 
    created_at : datetime
    updated_at : datetime

    model_config = ConfigDict(from_attributes=True) #allows Pydantic to build responses directly SQLAlchemy Repository object's attribute
        


