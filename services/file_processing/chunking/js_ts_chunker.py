
from schemas.chunk import ChunkRawWithNoEmbedding
from .line_based_chunker import create_line_based_chunks

import tree_sitter_javascript 
import tree_sitter_typescript

from tree_sitter import Language, Parser

JAVASCRIPT_LANGUAGE = Language(tree_sitter_javascript.language())
JS_PARSER = Parser(JAVASCRIPT_LANGUAGE)

TYPESCRIPT_LANGUAGE = Language(tree_sitter_typescript.language_typescript())
TS_PARSER = Parser(TYPESCRIPT_LANGUAGE)

TSX_PARSER = Parser(Language(tree_sitter_typescript.language_tsx()))


def create_javascript_typescript_chunks(text_content : str, file_id: int, suffix : str) -> list[ChunkRawWithNoEmbedding]:

    parser_by_suffix = {
        ".js" : JS_PARSER,
        ".jsx" : JS_PARSER,
        ".ts" : TS_PARSER,
        ".tsx" : TSX_PARSER
    }

    #get the correct JS or TS parser
    parser = parser_by_suffix.get(suffix)

    #invalid suffix -> fallback
    if parser is None: 
        return create_line_based_chunks(text_content, file_id)

    #Tree-sitter parse Bytes
    source_bytes = text_content.encode("utf-8")
    tree = parser.parse(source_bytes)

    #parser error -> fallback
    if tree.root_node.has_error:
        return create_line_based_chunks(text_content, file_id)

    chunks : list[ChunkRawWithNoEmbedding] = []
    import_nodes = []

    #helper function to read the text context (decode bytes back into readable text)
    def get_node_text(node) -> str: 
        return source_bytes[node.start_byte : node.end_byte].decode("utf-8")

    #Traverse the tree recursively 
    def visit(node, current_class_name : str | None=None) -> None:

         #preserve the enclosing class/interface name
        class_name = current_class_name

        if node.type == "import_statement":
            import_nodes.append(node)
            return 

        # get the current class/interface name
        if node.type in {
            "class_declaration",
            "abstract_class_declaration",
            "interface_declaration"
        }:         
            name_node = node.child_by_field_name("name")

            if name_node is not None: #there might not be a class name
                class_name = get_node_text(name_node)

        #Get standalone function declarations
        if node.type in {
            "function_declaration",
            "generator_function_declaration"
        }:
            name_node = node.child_by_field_name("name")

            if name_node is not None:
                chunks.append(ChunkRawWithNoEmbedding(
                    text_content=get_node_text(node),
                    start_line=node.start_point.row + 1,
                    end_line=node.end_point.row + 1,
                    class_name=None, 
                    func_name=(
                        get_node_text(name_node)
                        if name_node is not None
                        else None
                    ),
                    chunk_type="function",
                    file_id=file_id
                ))
            return

        # get Class or Interface methods 
        if node.type in {
            "method_definition",
            "abstract_method_signature",
        }:
            name_node = node.child_by_field_name("name")

            if name_node is not None:
                chunks.append(ChunkRawWithNoEmbedding(
                    text_content=get_node_text(node),
                    start_line=node.start_point.row + 1,
                    end_line=node.end_point.row + 1,
                    class_name=class_name,
                    func_name=(
                        get_node_text(name_node)
                        if name_node is not None
                        else None
                    ),
                    chunk_type="method",
                    file_id=file_id
                ))
            return 

        # checks whether a JS variable stores a function
        # example: const add = (a, b) => a + b;
            # name_node gets the variable name, such as add.
            # value_node gets the assigned value, such as the arrow function.
        if node.type == "variable_declarator": 
            name_node = node.child_by_field_name("name")
            value_node = node.child_by_field_name("value")

            if (name_node is not None and value_node is not None and 
                value_node.type in {
                    "arrow_function",
                    "function_expression",
                    "generator_function",
            }):

                #prefer the parent declaration so the chunk includes const, let, or var when available
                chunk_node = (
                    node.parent
                    if node.parent is not None
                    else node
                )

                chunks.append(ChunkRawWithNoEmbedding(
                    text_content=get_node_text(chunk_node),
                    start_line=chunk_node.start_point.row + 1,
                    end_line=chunk_node.end_point.row + 1,
                    class_name=class_name,
                    func_name=get_node_text(name_node),
                    chunk_type="function",
                    file_id=file_id
                ))

                return 

        for child in node.named_children:
            visit(child, class_name)

    visit(tree.root_node)

    #combine imports into 1 chunk
    if import_nodes:
        import_text = "\n".join(
            get_node_text(node)
            for node in import_nodes
        )

        chunks.insert(0, ChunkRawWithNoEmbedding(
            text_content=import_text,
                start_line=import_nodes[0].start_point.row + 1,
                end_line=import_nodes[-1].end_point.row + 1,
                class_name=None,
                func_name=None,
                chunk_type="imports",
                file_id=file_id,
            )
        )

    if not chunks:
        return create_line_based_chunks(text_content, file_id)

    return chunks


            
