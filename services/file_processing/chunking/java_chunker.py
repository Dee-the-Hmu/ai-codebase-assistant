
from schemas.chunk import ChunkRawWithNoEmbedding
import tree_sitter_java # Java's Tree-sitter grammar (defines syntax such as classes, methods, fields, statements)
from tree_sitter import Language, Parser #Langague wraps a language grammar so Tree-sitter can use it, Parser = reads src code and produces a syntax tree

from .line_based_chunker import create_line_based_chunks

#for java files
JAVA_LANGUAGE = Language(tree_sitter_java.language()) #get the Java grammar from tree_sitter_java, converts it to a Tree-sitter Language object
JAVA_PARSER = Parser(JAVA_LANGUAGE) #parser for Javc

def create_java_chunks(text_content: str, file_id: int) -> list[ChunkRawWithNoEmbedding]:

    #Tree-sitter parse Bytes    source_bytes = text_content.encode("utf-8") 
    source_bytes = text_content.encode()
    tree = JAVA_PARSER.parse(source_bytes)

    #parser error -> fallback
    if tree.root_node.has_error:
        return create_line_based_chunks(text_content, file_id)

    chunks : list[ChunkRawWithNoEmbedding] = []
    header_nodes = []

    def get_node_text(node) -> str: #decode the text for the chunk back 
        return source_bytes[node.start_byte : node.end_byte].decode("utf-8")

    def visit(node, current_class_name : str | None = None) -> None:

        if node.type in { 
            "import_declaration",
            "package_declaration",
        }:
            header_nodes.append(node)
            
        # get class name
        if node.type in {
            "class_declaration",
            "interface_declaration",
            "enum_declaration",
            "record_declaration"
        }:
            name_node = node.child_by_field_name("name")
            if name_node is not None:  #there might not be a class name
                class_name = get_node_text(name_node)

        #class body - get method name
        if node.type in {
            "method_declaration",
            "constructor_declaration"
        }:
            name_node = node.child_by_field_name("name")

            if name_node is not None:
                chunks.append(ChunkRawWithNoEmbedding(
                    text_content=get_node_text(node),
                    start_line=node.start_point.row + 1,
                    end_line=node.end_point.row + 1,
                    class_name=class_name,
                    func_name=get_node_text(name_node),
                    chunk_type=(
                        "constructor" #for constructor instead of method
                        if node.type == "constructor_declaration"
                        else "method"
                    ),
                    file_id=file_id
                )
                )

        #visit curr_node's childern
        for child in node.named_childern:
            visit(child, class_name)

    #start visiting from the root
    visit(tree.root_node)

    #for imports and package declaration
    if header_nodes:
        header_text = "\n".join(get_node_text(node) for node in header_nodes)

    #put that at the front of the chunks list
    chunks.insert(0, ChunkRawWithNoEmbedding(
        text_content=header_text,
        start_line=header_nodes[0].start_point.row+1,
        end_line=header_nodes[-1].end_point.row+1,
        class_name=None,
        func_name=None,
        chunk_type="package_and_imports",
        file_id=file_id
    ))

    #no ChunkRawWithNoEmbedding in the chunks list
    if not chunks: #fallback if java chunking fails 
        return create_line_based_chunks(text_content, file_id)

    return chunks