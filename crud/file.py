
from models.file import File
from schemas.file import FileCreate, FileUpdate

from sqlalchemy.orm import Session
from sqlalchemy import select

def create_file(db : Session, file_data : FileCreate) -> File: 
    new_file = File(
        path=file_data.path,
        name=file_data.name,
        size_bytes=file_data.size_bytes,
        repo_id=file_data.repo_id
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return new_file


def read_file_with_id(db : Session, file_id : int) -> File | None: 
    statement = select(File).where(
        File.id == file_id
    )
    return db.scalar(statement)


def read_file_with_name_and_repo_id(db : Session, file_name : str, repo_id : int) -> File | None:
    statement = select(File).where(
        File.name == file_name, 
        File.repo_id == repo_id
    )
    return db.scalar(statement)


def update_file(db : Session, file : File, file_data : FileUpdate) -> File: 
    # convert Pydantic object into Dict 
    update_data = file_data.model_dump(exclude_unset=True)

    for field,value in update_data.items():
        setattr(file, field, value)

    db.commit()
    db.refresh(file)

    return file


def delete_file_with_id(db : Session, file_id : int) -> bool: 
    
    file = db.get(File, file_id)

    if file is None: 
        return False

    db.delete(file)
    db.commit()

    return True

