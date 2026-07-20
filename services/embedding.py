from sentence_transformers import SentenceTransformer

MODEL_NAME = "jinaai/jina-embeddings-v2-base-code"

# load the model 
model = SentenceTransformer(
    MODEL_NAME,
    trust_remote_code=True
)

dimension = model.get_embedding_dimension()

def embed_code_chunk(searchable_text : str) -> list[float]:
    if not searchable_text.strip():
        raise ValueError("searchable_text cannot be empty")
    
    embeddings = model.encode_document( #encode code chunk using encode_document() and user's query using encode_query()
        searchable_text,
        normalize_embeddings=True #scales each vector to unit length
    )

    return embeddings.tolist()

def embed_user_question(query : str) -> list[float]:
    if not query.strip():
        raise ValueError("query cannot be empty")
    
    embedding = model.encode_query(
        query,
        normalize_embeddings=True
    )

    return embedding.tolist()