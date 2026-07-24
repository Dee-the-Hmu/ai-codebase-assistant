import json
from schemas.chunk import ChunkRawWithNoEmbedding
from .line_based_chunker import create_line_based_chunks

def create_json_chunks(text_content : str, file_id : int) -> list[ChunkRawWithNoEmbedding]:

    try:
        # loads = converts JSON into Python objects
        parsed_json = json.loads(text_content)
    except json.JSONDecodeError:
        return create_line_based_chunks(text_content, file_id)

    chunks: list[ChunkRawWithNoEmbedding] = []

    # for key-value pair dict -> embed each key-value pair 
    if isinstance(parsed_json, dict):

        #iterate the dictionary
        for key, value in parsed_json.items():

            #json.dumps() converts Python data into JSON 
            chunk_text = json.dumps(
                {key : value}, #creates a new dict containing 1 key-value pair 
                indent=2,  # makes the JSON readable 
                ensure_ascii=False #stores non-English characters normally
            )

            #embed each key-value pair for better retrieval, key becomes the function name
            append_json_chunks(chunks=chunks, text_content=chunk_text, file_id=file_id, func_name=str(key), chunk_type="json_object")

    # for list
    elif isinstance(parsed_json, list):

        #iterate the list
        for index, value in enumerate(parsed_json):

            # converts Python data into JSON
            chunk_text = json.dumps(
                value, #only write the element
                indent=2,
                ensure_ascii=False,
            )

            #embed each value, index becomes the function name (array index)
            append_json_chunks(chunks=chunks, text_content=chunk_text, file_id=file_id, func_name=str(index), chunk_type="json_array_item")

    # else, embed the whole json file as one
    else: 
        entire_chunk_context = json.dumps(
            parsed_json,
            indent=2,
            ensure_ascii=False
        )

        append_json_chunks(chunks=chunks, text_content=entire_chunk_context, file_id=file_id, func_name=None, chunk_type="json_value")

    #JSON parsing produces no chunks
    if not chunks:
        return create_line_based_chunks(text_content=text_content, file_id=file_id)

    return chunks


def append_json_chunks(chunks : list[ChunkRawWithNoEmbedding], text_content : str, file_id : int, func_name : str | None, chunk_type : str) -> None:

    chunks.append(ChunkRawWithNoEmbedding(
        text_content=text_content,
        start_line=None,
        end_line=None,
        class_name=None,
        func_name=func_name,
        chunk_type=chunk_type,
        file_id=file_id
    ))
        
    
