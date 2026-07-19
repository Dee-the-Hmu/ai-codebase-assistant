from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class Repository(Base):
    __tablename__ = "repositories"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    files: Mapped[list["File"]] = relationship(back_populates="repository")  #files = a list of "File" objects
    """
    files = a list of "File" objects
    1 repository can have many files 
    back_populate="repository" 
        points to the attribute named "repository" inside the File class

    SQLAlchemy connects these 2 attributes: Repository.files  ↔  File.repository

    actual database connection come from repo_id: Mapped[int] = mapped_column(ForeignKey("repositories.id))
    """
