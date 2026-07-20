"""
Before we create a Chunk, 
    get the text context and its metadata
    make a searchable_text
    convert it to vector embedding
    creates ChunkCreate
    then calls curd.create_chunk()
"""

from .searchable_text import build_searchable_text
from .embedding import embed_code_chunk, embed_code_chunks
from schemas.chunk import ChunkCreate, ChunkRawWithNoEmbedding
from crud.file import read_file_and_repo_with_file_ids
from crud.chunk import create_chunk, create_chunks
from models.chunk import Chunk

from sqlalchemy.orm import Session


#for 1 chunk
def create_chunk_with_embed(db : Session, chunk_data_with_no_embedding : ChunkRawWithNoEmbedding) -> Chunk | None:

    #chunk_data has file_id -> find the file with this file_id to get its info
    file_dict_with_id = read_file_and_repo_with_file_ids(db, [chunk_data_with_no_embedding.file_id]) #use read_file_and_repo_with_file_ids to avoid lazy loading

    file = file_dict_with_id.get(chunk_data_with_no_embedding.file_id)

    if file is None:
        return None
    
    repo = file.repository # no longer lazy loading

    #make a searchable_text
    searchable_text = build_searchable_text(
        repo_name=repo.name,
        file_path=file.path,
        class_name=chunk_data_with_no_embedding.class_name,
        func_name=chunk_data_with_no_embedding.func_name,
        text_content=chunk_data_with_no_embedding.text_content
    )

    #convert it to vector embedding
    embedding = embed_code_chunk(searchable_text=searchable_text)

    #creates a ChunkCreate
    chunk_data_with_embedding = ChunkCreate(
        **chunk_data_with_no_embedding.model_dump(), #converts the Pydantic model into a dictionary, ** = unpacks the dict into named keyword arguments
        embedding=embedding
    )

    #calls curd.chunk_create() -> commits to database
    chunk = create_chunk(db, chunk_data=chunk_data_with_embedding)

    return chunk


# for a list of chunks
def create_chunks_with_embeddings(db : Session, chunk_datas_with_no_embeddings: list[ChunkRawWithNoEmbedding]) -> list[Chunk]:
    
    file_ids : set[int] = set() #use set to remove duplicate file_id
    searchable_texts = []

    # get the file_ids of all ChunkRawWithNoEmbeddings
    for chunk_data_with_no_embedding in chunk_datas_with_no_embeddings: 
        file_ids.add(chunk_data_with_no_embedding.file_id)

    file_ids = list(file_ids)

    # get the file and repo from the file_ids
    files_dict_with_id = read_file_and_repo_with_file_ids(db, file_ids=file_ids) #returns dict[file_id, file]

    # create searachable_texts from the the chunk_data for all ChunkRawWithNoEmbeddings
    for chunk_data_with_no_embedding in chunk_datas_with_no_embeddings:
        file = files_dict_with_id.get(chunk_data_with_no_embedding.file_id)

        if file is None:
            raise ValueError(f"\nFile with id {chunk_data_with_no_embedding.file_id} does NOT exist!")

        searchable_text = build_searchable_text(
            repo_name=file.repository.name,
            file_path=file.path,
            class_name=chunk_data_with_no_embedding.class_name,
            func_name=chunk_data_with_no_embedding.func_name,
            text_content=chunk_data_with_no_embedding.text_content
        )
        searchable_texts.append(searchable_text)

    # batch embeddings of all searchable_texts
    embeddings = embed_code_chunks(searchable_texts=searchable_texts)

    
    chunk_datas_with_embeddings = [] 

    #creates ChunkCreates for all Chunks + their embeddings
    for chunk_data_with_no_embedding, embedding in zip(chunk_datas_with_no_embeddings, embeddings, strict=True): #strict=True raise ValueError when the 2 lists have different lenghts
        
        chunk_datas_with_embeddings.append(ChunkCreate(
        **chunk_data_with_no_embedding.model_dump(), #converts the Pydantic model into a dictionary, ** = unpacks the dict into named keyword arguments
        embedding=embedding
    ))

    #calls curd.chunk_creates() -> commits to database (Bulk insert in 1 transaction)
    created_chunks = create_chunks(db, chunk_datas=chunk_datas_with_embeddings)

    return created_chunks

