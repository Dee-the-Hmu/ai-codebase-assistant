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
    tree.body = a list containing the top-level statements in the paresed Python file
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

        # if it is a function (top level function)
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

            class_level_nodes = []
        
            #loop thru the class
            for class_node in node.body:

                #method inside the class
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

                #class-level content (lines outside methods)
                # Pydantic attributes, SQLAlchemy columns 
                # class docstring
                else:
                    class_level_nodes.append(class_node)

            if class_level_nodes:
                class_parts = [source_lines[node.lineno-1]]
                class_end_line = node.lineno #just to initialize 

                for class_node in  class_level_nodes:
                    if class_node.end_lineno is None:
                        continue

                    #add only that node's line (this is so that not to include the methods between class-lvl contents)
                    class_part = "\n".join(source_lines[class_node.lineno - 1 : class_node.end_lineno])

                    class_parts.append(class_part)
                    class_end_line = max(class_end_line, class_node.end_lineno)

                chunk_text = "\n".join(class_parts)

                chunks_raw.append(ChunkRawWithNoEmbedding(
                    text_content=chunk_text,
                    start_line=node.lineno,
                    end_line=class_end_line,
                    class_name=node.name, 
                    func_name=None,
                    chunk_type="class",
                    file_id=file_id
                ))

    return chunks_raw
