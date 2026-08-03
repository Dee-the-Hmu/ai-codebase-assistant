from fastapi import FastAPI 
from routers.repositories import router as repositories_router
from routers.questions import router as questions_router

app = FastAPI()

app.include_router(repositories_router)
app.include_router(questions_router)