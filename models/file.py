from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from .base import Base

class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    repo_id: Mapped[int] = mapped_column(ForeignKey("repositories.id")) #repo_id attribute must match with the "id" column in the "repositories table"

    repository: Mapped["Repository"] = relationship(back_populates="files")
    """
    repository = will hold 1 related Repository object 
    backpopulate="files"
        points the attribute named "files" inside the Repository class 

    connecting: Repository.files  ↔  File.repository
    """