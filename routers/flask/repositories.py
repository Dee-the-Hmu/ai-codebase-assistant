from flask import Blueprint, jsonify, request
from database import SessionLocal
from crud.repository import read_all_repo
from schemas.repository import RepositoryResponse, RepositoryIngestRequest

from pydantic import ValidationError
from services.repo_ingestion import ingest_repository

#groups related endpoints (same as FastAPI's APIRouter)
repositories_router = Blueprint(
    "repositories", #Blueprint name
    __name__, #Current module location
    url_prefix="/repositories" #prefix added to every route
)

"""
creates a repo (download, filter, chunk the files)
"""
@repositories_router.post("")
def create_repository_endpoint():
    db = SessionLocal()

    try: 
        #get the JSON body from the request as Python dictionary
        request_data = request.get_json()

        #validates the request_data and converts it into RepositoryIngestRequest Pydantic model
        validated_request = RepositoryIngestRequest.model_validate(request_data)

        #validate the github repo url, download, chunk and embeds
        repo = ingest_repository(db=db, github_url=validated_request.github_url)

        if repo is None:
            #returns a JSON error response with HTTP status 
            return jsonify(
                {
                    "detail" : (
                        "Repository could not be ingested "
                        "or already exists."
                    ),
                },
            ), 400

        #converts the returned SQLAlchemy ORM object into Pydantic Model RespositoryResponse then to JSON safe data (like a dict)
        response_data = RepositoryResponse.model_validate(repo).model_dump(mode="json")

        #converts the dict into json 
        return jsonify(response_data), 201

    except ValidationError as error:
        # returns a JSON error response
        return jsonify(
            {
                "detail" : error.errors()
            }
        ), 422

    finally:
        db.close()

"""
repositories contains SQLAlchemy ORM objects, and 
Flask cannot directly convert them to JSON.

"""
@repositories_router.get("")
def get_all_repos():
    db = SessionLocal()

    try: 
        repositories = read_all_repo(db=db)

        response_data =[]

        for repo in repositories:
            #converts each ORM object into Pydantic RepositoryResponse model
            #model_dump(...) converts the Pydantic RepositoryResponse model to JSON-safe data (like dict)
            data = RepositoryResponse.model_validate(repo).model_dump(mode="json")
            response_data.append(data)

        #jsonify() creates the HTTP JSON Response
        return jsonify(response_data), 200
    finally:
        db.close()

