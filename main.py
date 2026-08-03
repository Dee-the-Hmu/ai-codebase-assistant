from fastapi import FastAPI 
from routers.repositories import router as repositories_router
from routers.questions import router as questions_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Codebase Assistant",
    verion="1.0.0"
)

"""
Browsers block frontend requests to a different origin unless the backend explicitly permits them.
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(repositories_router)
app.include_router(questions_router)