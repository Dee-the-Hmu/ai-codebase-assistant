from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas.question import QuestionRequest, QuestionResponse
from services.answer_question import retrieve_related_chunks, answer


router = APIRouter(prefix="/repositories",
                   tags=["questions"])

@router.post(
    "/{repo_id}/questions",
    response_model=QuestionResponse,
    status_code=status.HTTP_200_OK
    )
def ask_question(
    repo_id : int,
    request : QuestionRequest,
    db : Session = Depends(get_db),
) -> QuestionResponse:

    #get related_chunks (compare cosine distance with the user's question's vector embedding with the chunk's embedding in the database)
    related_chunks = retrieve_related_chunks(
        db=db,
        question=request.question, 
        repo_id=repo_id
    )

    answer_text, citation_list = answer(
        related_chunks=related_chunks, 
        question=request.question
        )

    return QuestionResponse(
        answer=answer_text, 
        citations=citation_list
        )
    