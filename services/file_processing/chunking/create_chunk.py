"""
gets the text_content of a file, file_path, file_id: int
must chunk by logical units  DEPENDING on the Language
- use Python's built-in ast module for .py files --? fallback if parsing fail for SyntaxError?
- use Tree-sitter for other languages 

Steps to chunk by logical units 
    1 function per chunk
    1 method per chunk
    1 small class per chunk
    module_level imports/constants grouped separately

    large functions ->split only when they exceed the embedding limit NEED TO DO 

    for documentation
        .md files = markdown by headings and sections
        fallback line-based chunks 
        JSON by meaningful top-level objects 

  
    keep a token/line-based fallback for unsupported files or parser failures

"""
from pathlib import Path
from schemas.chunk import ChunkRawWithNoEmbedding

from .line_based_chunker import create_line_based_chunks
from .python_chunker import create_python_chunks
from .java_chunker import create_java_chunks
from .js_ts_chunker import create_javascript_typescript_chunks
from .markdown_chunker import create_markdown_chunks
from .json_chunker import create_json_chunks

def create_chunks(text_content : str, relative_file_path_str : str, file_id : int) -> list[ChunkRawWithNoEmbedding]:
    
    suffix = Path(relative_file_path_str).suffix.lower()

    #is it python file --> AST chunking (ast.parse() raises SyntaxError when the Python source cannot be parsed)
    if suffix == ".py": 
        try:
            return create_python_chunks(text_content, file_id)
        except (SyntaxError, ValueError):  #python syntax failure --> failback 
            return create_line_based_chunks(text_content, file_id)

    #is it Java file --> use tree sitter
    if suffix == ".java":
        return create_java_chunks(text_content, file_id)
        
    #is it JavaScript, TypeScript file --> use tree sitter
    if suffix in {".js", ".jsx", ".ts", ".tsx"}:
        return create_javascript_typescript_chunks(text_content, file_id, suffix=suffix)

    #is it markdown 
    if suffix == ".md":
        return create_markdown_chunks(text_content, file_id)

    #is it JSON
    if suffix == ".json":
        return create_json_chunks(text_content, file_id)
    
    #next for other languages Tree-sitter CONTINUE HERE
    #later 

    #every other file --> line based fallback
    return create_line_based_chunks(text_content, file_id)
    


    
