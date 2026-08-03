"""
get the user's question from the frontend
embed the question
compare with all the embeddings we have

sends a good amount of chunks with the question to LLM
answers the question
"""

from sqlalchemy.orm import Session
from .embedding import embed_user_question
from models.chunk import Chunk
from crud.chunk import semantic_search_chunks
from schemas.config import settings
from schemas.question import CitationResponse

from openai import OpenAI 

MODEL_NAME = "gpt-5.4-nano"  # cheapest model 

client = OpenAI(api_key=settings.openai_api_key)

"""
get the user's question from the frontend
embed the question
compare with all the embeddings we have
"""
def retrieve_related_chunks(db : Session, question : str, repo_id : int) -> list[tuple[Chunk, float]]:

    #embed the question
    question_embedding = embed_user_question(question)

    #get the related chunks 
    return semantic_search_chunks(
        db=db,
        query_embedding=question_embedding,
        limit = 10, #10 chunks 
        repo_id=repo_id
    )

system_prompt="""
You are an AI assistant that answers questions about a software repository.

You must answer only using the repository context provided to you.

Rules:

1. Do not use outside knowledge.
2. Do not invent files, functions, classes, variables, behavior, or line numbers.
3. Every claim about the repository must be supported by at least one citation.
4. Use citations in this exact format:

[file_path:start_line-end_line]

5. Use only the exact file path and complete line range shown in a SOURCE block. Do not create, shorten, expand, or estimate line ranges.
6. Explain both:
   * what the code does
   * how the relevant code works to accomplish it
7. When multiple files or functions work together, explain their relationship clearly.
8. Do not assume behavior that is not directly visible in the provided code.
9. If the context is incomplete, say:

“I could not determine that from the retrieved repository context.”

10. If only part of the question can be answered, answer that part and clearly state what cannot be determined.
11. Do not present guesses as facts.
12. Keep the answer clear and focused.

Format the answer using exactly this structure:

SUMMARY: <brief overall summary>

STEP: <short step title>
<first explanation line>
<second explanation line>
<third explanation line>
CITATION: [exact_file_path:exact_start_line-exact_end_line]

Repeat the STEP and CITATION sections as needed.

Rules:
- Begin with exactly one SUMMARY line.
- Begin every explanation section with STEP: followed by a short title.
- Write the explanation for each step as multiple short lines.
- Put each distinct action or behavior on its own line.
- Do not combine the entire explanation into one paragraph.
- End every step with exactly one CITATION line.
- Use only an exact file path and exact complete line range provided in a SOURCE block.
- Do not invent, shorten, expand, or estimate citation ranges.
- Do not use markdown headings, numbered lists, or bullet points.
"""

"""
sends the context (combined chunks) and the question to LLM 
add strict prompt 
    LLM answers the question
returns the answer, list of CitationResponse
"""
def answer(related_chunks : list[tuple[Chunk, float]], question : str) -> tuple[str, list[CitationResponse]]:

    #empty retrieval 
    if not related_chunks:
        return (
            "I could not determine that from the retrieved repository context.", 
            []
        )

    #combine all the related chunks -> context str
    context_str = helper_build_context_from_related_chunks(related_chunks)

    #citation_list (information about the chunks the model use to answer the question)
    citation_list = helper_build_citation_list(related_chunks)
    
    text_response = client.responses.create(
        model=MODEL_NAME,
        instructions=system_prompt,
        input=f"""
Repository context: 

{context_str}

User question:

{question}
"""
    )

    answer_text = text_response.output_text
    

    return answer_text, citation_list

"""
combine all the related chunks together as a string
"""
def helper_build_context_from_related_chunks(related_chunks : list[tuple[Chunk, float]]) -> str:
    contexts_list = []

    for src_number, (chunk, cosine_distance) in enumerate(related_chunks, start=1): #src number = chunk's position in the retrived results 
        context = f"""
SOURCE: {src_number}
File: {chunk.file.path}
Line Number: {chunk.start_line} to {chunk.end_line}
Class: {chunk.class_name}
Function: {chunk.func_name}
Chunk type: {chunk.chunk_type}

{chunk.text_content}
""".strip()

        contexts_list.append(context)

    context_str = "\n\n".join(contexts_list)

    return context_str


"""
get a list of citation (only file paths and line ranges)
"""
def helper_build_citation_list(related_chunks : list[tuple[Chunk, float]]) -> list[CitationResponse]:

    citation_list = []

    for chunk, cosine_distance in related_chunks:

        #smaller distance = higher similarity 
        similarity_score = max( #to not go above 1 or below 0
            0.00,
            min(1, 1 - cosine_distance))

        citation_list.append(
            CitationResponse(
                file_path=chunk.file.path,
                start_line=chunk.start_line,
                end_line=chunk.end_line,
                similarity_score=similarity_score
            )
        )

    return citation_list