"""
adds metadata to code chunk before converting into a vector embeddings for better retrieval
"""

def build_searchable_text(
        repo_name : str,
        file_path : str,
        class_name : str | None,
        func_name : str | None,
        text_content : str
) -> str: 
    
    words_list = [
        f"Repository: {repo_name}",
        f"File: {file_path}",
    ]

    if class_name is not None: 
        words_list.append(f"Class: {class_name}")
    if func_name is not None:
        words_list.append(f"Function: {func_name}")

    words_list.append(f"Code:\n{text_content}")

    searchable_text = "\n".join(words_list)

    return searchable_text