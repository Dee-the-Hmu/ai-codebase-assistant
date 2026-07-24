from schemas.chunk import ChunkRawWithNoEmbedding

def create_markdown_chunks(text_context : str, file_id : int) -> list[ChunkRawWithNoEmbedding]:

    #split all lines by \n
    lines = text_context.splitlines()

    chunks : list[ChunkRawWithNoEmbedding] = []

    #index start = line start - 1
    section_start_index = 0

    #current heading is None
    current_heading : str | None = None

    #iterate thru each line
    for index, line in enumerate(lines):
        stripped_line = line.lstrip() #removes the character from left side to get "### Heading"

        # is it right markdown heading?
        if stripped_line.startswith("#"): 
            heading_parts = stripped_line.split(maxsplit=1) #at most 1 split (e.g."hello world again".split(maxsplit=1) --> ["hello", "world again"] )

            #check if it is a valid Markdown Heading (# Heading to ###### Heading)
            if ( len(heading_parts[0]) <= 6 
                and set(heading_parts[0]) == {'#'} 
                and 
                    (len(stripped_line) == len(heading_parts[0]) # the line is only ### == ###
                    or stripped_line[len(heading_parts[0])] == ' ' #there a space afeter # or ### like "### Titile"
                    )
            ):

                #this saves the section above the valid header
                text_content = "\n".join(lines[section_start_index : index]).strip()

                if text_content: 
                    chunks.append(ChunkRawWithNoEmbedding(
                        text_content=text_content,
                        start_line=section_start_index+1, # since section_start_index is 0-indexed
                        end_line=index,
                        class_name=None,
                        func_name=current_heading, #this is previous heading (the heading before we found another valid heading)
                        chunk_type="markdown_section",
                        file_id=file_id,
                    ))

                #update the start index to the end index
                section_start_index = index

                if len(heading_parts) > 1: #newly validated heading has Heading Title
                    current_heading = heading_parts[1].strip() ### Heading, heading_parts[1]= Heading
                else:
                    current_heading = None

    #the last section was not saved (since we save the text_content only when we found a new valid heading)
    final_section_text = "\n".join(lines[section_start_index : len(lines)]).strip()

    if final_section_text: 
        chunks.append(ChunkRawWithNoEmbedding(
                        text_content=final_section_text,
                        start_line=section_start_index+1, # 0-indexed
                        end_line=len(lines),
                        class_name=None,
                        func_name=current_heading,
                        chunk_type="markdown_section",
                        file_id=file_id,
                        )
                    )

    return chunks



