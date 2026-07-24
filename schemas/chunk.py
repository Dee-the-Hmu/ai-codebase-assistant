from pydantic import BaseModel, ConfigDict

class ChunkBase(BaseModel):
    text_content : str
    start_line : int | None = None
    end_line : int | None = None
    class_name : str | None = None
    func_name : str | None = None
    chunk_type : str
    # embedding : list[float]
    metadata_ : dict | None = None
    file_id : int 

class ChunkRawWithNoEmbedding(ChunkBase):
    pass

class ChunkUpdate(BaseModel):
    text_content : str | None = None
    start_line : int | None = None
    end_line : int | None = None
    class_name : str | None = None
    func_name : str | None = None
    chunk_type : str | None = None
    embedding : list[float] | None = None
    metadata_ : dict | None = None #because the SQLAlchemy attribute is metadata_
    file_id : int | None = None

class ChunkCreate(ChunkBase):
    embedding : list[float]
    pass

class ChunkResponse(ChunkBase):
    id : int 
    embedding : list[float]

    model_config = ConfigDict(from_attributes=True) #allows Pydantic to build responses from SQLAlchemy Chunk object's attributes



