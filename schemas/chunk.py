from pydantic import BaseModel, ConfigDict

class ChunkBase(BaseModel):
    text_content : str
    start_line : int
    end_line : int
    func_or_class_name : str | None = None
    chunk_type : str
    embedding : list[float]
    metadata_ : dict | None = None
    file_id : int 

class ChunkUpdate(BaseModel):
    text_context : str | None = None
    start_line : str | None = None
    end_line : str | None = None
    func_or_class_name : str | None = None
    chunk_type : str | None = None
    embedding : list[float] | None = None
    metadata_ : dict | None = None #because the SQLAlchemy attribute is metadata_
    file_id : int | None = None

class ChunkCreate(ChunkBase):
    pass

class ChunkResponse(ChunkBase):
    id : int 

    model_config = ConfigDict(from_attributes=True) #allows Pydantic to build responses from SQLAlchemy Chunk object's attributes



