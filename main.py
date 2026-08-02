from fastapi import FastAPI 
from routers.repositories import router as repositories_router

app = FastAPI()

app.include_router(repositories_router)