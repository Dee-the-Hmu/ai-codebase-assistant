from .line_based_chunker import create_line_based_chunks
import ast #Python's built-in ast module for .py files 
from schemas.chunk import ChunkRawWithNoEmbedding


#if the file is a Python file
def create_python_chunks(text_content : str, file_id : int) -> list[ChunkRawWithNoEmbedding]:
    
    tree = ast.parse(text_content) #tree = root of the syntax tree

    source_lines = text_content.splitlines()

    chunks_raw : list[ChunkRawWithNoEmbedding] = []

    """ 
    node = 1 top-lvl Python statement = 1 syntax structure 
    tree.body = a list containint the top-level statements in the paresed Python file
    """

    #handle import(s)
    import_chunks: list[str] = []

    import_nodes = []

    #gets all import lines/nodes
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            import_nodes.append(node)

    #take each import line and put that in import_chunks
    if import_nodes:
        for import_node in import_nodes:
            start_line = import_node.lineno
            end_line = import_node.end_lineno

            import_text = "\n".join(
                source_lines[start_line-1 : end_line]
            )

            import_chunks.append(import_text)

    #combine all import_chunks as a text_content
    if import_chunks:
        chunk_text = "\n".join(import_chunks)

        chunks_raw.append(ChunkRawWithNoEmbedding(
            text_content=chunk_text,
            start_line=import_nodes[0].lineno,
            end_line=import_nodes[-1].end_lineno,
            class_name=None,
            func_name=None,
            chunk_type="imports",
            file_id=file_id
        ))

    # handle function and class
    for node in tree.body: 

        # if it is a function
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)): 
            start_line = node.lineno #lineno starts count from 1
            end_line = node.end_lineno #end of that syntax structure (end of function)

            chunk_text = "\n".join(source_lines[start_line-1 : end_line]) # all lines of that function

            #append/creates ChunkRawWithNoEmbedding -> ready to be used to generate embeddings
            chunks_raw.append(ChunkRawWithNoEmbedding(
                text_content=chunk_text,
                start_line=start_line,
                end_line=end_line,
                class_name=None,
                func_name=node.name,
                chunk_type="function",
                file_id=file_id
            ))

        #if a class
        elif isinstance(node, ast.ClassDef):

            #loop thru the class
            for class_node in node.body:
                
                if isinstance(class_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    start_line = class_node.lineno
                    end_line = class_node.end_lineno

                    chunk_text = "\n".join(
                        source_lines[start_line-1 : end_line]
                    )

                    #append/creates ChunkRawWithNoEmbedding -> ready to be used to generate embeddings
                    chunks_raw.append(ChunkRawWithNoEmbedding(
                        text_content=chunk_text,
                        start_line=start_line,
                        end_line=end_line,
                        class_name=node.name,
                        func_name=class_node.name,
                        chunk_type="method",
                        file_id=file_id
                    ))

    return chunks_raw
