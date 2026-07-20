from pydantic import BaseModel, ConfigDict
from datetime import datetime

class FileBase(BaseModel):
    repo_id : int
    path : str
    name : str
    size_bytes : int | None = None

class FileUpdate(BaseModel):
    repo_id : int | None = None
    path : str | None = None
    name : str | None = None
    size_bytes : int | None = None 

class FileCreate(FileBase):
    pass

class FileResponse(FileBase):
    id : int 
    created_at : datetime
    updated_at : datetime

    model_config = ConfigDict(from_attributes=True) #allows Pydantic to build responses directly from SQLAlchemy Repository object's attribute


