from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session 

from schemas.config import settings

from collections.abc import Generator #Generator type for describing a function that uses "yield"

#engine = manages database connections
engine = create_engine(settings.database_url) # main object that connects Python application to PostgreSQL 

#Session factory, calling this creates a new database session
SessionLocal = sessionmaker( # creates a factory that can produce database Session objects 
    bind=engine, # tells each session to connect to my database engine 
    autoflush=False, #prevents SQLAlchemy from auto sending pending changes to the database
    expire_on_commit=False # keep ORM object attributes after db.commit()
)

"""
generator = a function that PAUSES and RESUMES instead of finishing all at once
syntax = Generator[yield_type, send_type, return_type]
"""

def get_db() -> Generator[Session, None, None]: 
    #Session: the function yields a database Session
    #None: nothing is sent back into the generator
    #None: the generator does not return a final value 

    db = SessionLocal() #creates a new database session

    try:
        yield db #temporarily gives the session to the FastAPI endpoint, yield = pauses the function instead of ending it like "return"
    finally:
        db.close() #close the session after the request finishes
    