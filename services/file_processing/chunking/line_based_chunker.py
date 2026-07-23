from schemas.chunk import ChunkRawWithNoEmbedding

#fall back function (a reliable fallback)
# chunk it with number of lines
def create_line_based_chunks(text_content: str, file_id: int, max_lines_per_chunk: int = 100) -> list[ChunkRawWithNoEmbedding]:

    lines = text_content.splitlines()

    chunks : list[ChunkRawWithNoEmbedding] = []

    for start_index in range(0, len(lines), max_lines_per_chunk): 
        end_index = min(start_index+max_lines_per_chunk, len(lines)) #stop of the line
        chunk_text = "\n".join(lines[start_index:end_index]).strip()

        if not chunk_text:
            continue

        chunks.append(
            ChunkRawWithNoEmbedding(
                text_content=chunk_text,
                start_line=start_index + 1,
                end_line= end_index, #1-100, end index is equal to end line
                class_name=None,
                func_name=None,
                chunk_type="line_based",
                file_id=file_id
            )
        )
    return chunks