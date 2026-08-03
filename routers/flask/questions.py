from flask import Blueprint, jsonify, request 
from database import SessionLocal 
from schemas.question import QuestionRequest, QuestionResponse
from services.answer_question import retrieve_related_chunks, answer

from pydantic import ValidationError

questions_router = Blueprint(
    "questions", #blueprint name
    __name__, #current module name
    url_prefix="/repositories"
)

@questions_router.post("/<int:repo_id>/questions")
def ask_question(repo_id : int):
    db = SessionLocal()

    try:
        #get the JSON body from the request as Python dict
        request_data = request.get_json()

        #validates the request_data and convert it into QuestionRequest Pydantic model
        validated_request = QuestionRequest.model_validate(request_data)

        #get related_chunks (compare cosine distance with the user's question's vector embedding with the chunk's embedding in the database)
        related_chunks = retrieve_related_chunks(
            db=db,
            question=validated_request.question,
            repo_id=repo_id
        )

        #get the answer from LLM 
        answer_text, citation_list = answer(
            related_chunks=related_chunks,
            question=validated_request.question
        )

        #converts the returned answer and list[CitationResponse] into JSON safe data
        response_data = QuestionResponse(
            answer=answer_text,
            citations=citation_list
        ).model_dump(mode="json")

        #convers the dict into json
        return jsonify(response_data), 200

    except ValidationError as error:
        return jsonify(
            {
                "detail" : error.errors()
            }
        ), 422

    finally:
        db.close()