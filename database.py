from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from schemas.config import settings

engine = create_engine(settings.database_url) # main object that connects Python application to PostgreSQL 


SessionLocal = sessionmaker( # creates a factory that can produce database Session objects 
    bind=engine, # tells each session to communicate with PostgreSQL through your SQLAlchemy engine
    autoflush=False,
    expire_on_commit=False # after committing, Python objects keep their loaded attribute values 
)
