
from models.chunk import Chunk
from schemas.chunk import ChunkCreate, ChunkUpdate

from sqlalchemy.orm import Session
from sqlalchemy import select

def create_chunk(db : Session, chunk_data : ChunkCreate) -> Chunk: 

    new_chunk = Chunk(
        text_content=chunk_data.text_content,
        start_line=chunk_data.start_line,
        end_line=chunk_data.end_line,
        class_name=chunk_data.class_name,
        func_name=chunk_data.func_name,
        chunk_type=chunk_data.chunk_type,
        embedding=chunk_data.embedding,
        metadata_=chunk_data.metadata_,
        file_id=chunk_data.file_id
    )

    db.add(new_chunk)
    db.commit()
    db.refresh(new_chunk)

    return new_chunk 


def read_chunk_by_id(db : Session, chunk_id : int) -> Chunk | None: 
    statement = select(Chunk).where(
        Chunk.id == chunk_id
    )
    return db.scalar(statement)


def read_all_chunks_by_file_id(db : Session, file_id : int) -> list[Chunk]:
    statement = select(Chunk).where(
        Chunk.file_id==file_id
    )

    return list(db.scalars(statement).all()) # *** only difference .all() returns all matching Chunk as a list 
    # if no chunks exist, return []


def update_chunk(db : Session, chunk : Chunk, chunk_data : ChunkUpdate) -> Chunk:
    update_data = chunk_data.model_dump(exclude_unset=True)

    for field,value in update_data.items():
        setattr(chunk, field, value)

    db.commit()
    db.refresh(chunk)

    return chunk


def delete_by_chunk_id_and_file_id(db : Session, chunk_id : int, file_id : int) -> bool:
    statement = select(Chunk).where(
        Chunk.file_id==file_id,
        Chunk.id==chunk_id
    )

    chunk = db.scalar(statement)

    if chunk is None:
        return False
    
    db.delete(chunk)
    db.commit()

    return True

