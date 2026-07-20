
from models.chunk import Chunk
from models.repository import Repository
from models.file import File

from schemas.chunk import ChunkCreate, ChunkUpdate

from sqlalchemy.orm import Session
from sqlalchemy import select

# for 1 chunk
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

# for multiple chunks
def create_chunks(db : Session, chunk_datas : list[ChunkCreate]) -> list[Chunk]: 

    chunks = []

    for chunk_data in chunk_datas:
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
        chunks.append(new_chunk)

    try:
        db.add_add(chunks)
        db.commit()

        for chunk in chunks:
            db.refresh(chunk)

        return chunks

    except Exception:
        db.rollback()
        raise



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


def semantic_search_chunks(db : Session, query_embedding : list[float], limit : int, file_id : int | None = None, repo_id : int | None = None) -> list[Chunk]:
    
    """
    SELECT * FROM chunks AS c 
    JOIN files as f ON f.id = c.file_id 
    WHERE 
    (:repo_id IS NULL OR f.repo_id = :repo_id)
    AND
    (:file_id IS NULL OR c.file_id = :file_id)
    ORDER BY 
    c.embedding <=> CAST(:query_embedding AS vector)
    LIMIT :limit;
    """
    # : means the value is supplied
    # <=> means cosine_similarity 
        # compares teh angle b/w them
            # cosine distance = 1 - cosine similarity
            # distance near 0 -> very similar 
            # larger distance -> less similar
    # CAST means convert the value from list[float] to vector 
    statement = select(Chunk)

    if repo_id is not None: 
        statement = statement.join(File).where(File.repo_id==repo_id)

    if file_id is not None:
        statement = statement.where(
            Chunk.file_id==file_id
        )

    statement = (statement
        .order_by(Chunk.embedding.cosine_distance(query_embedding)) 
        .limit(limit)
    )
    return list(db.scalars(statement).all())
