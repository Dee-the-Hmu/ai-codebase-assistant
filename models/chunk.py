from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text, String, JSON
from .base import Base 
from typing import TYPE_CHECKING

from pgvector.sqlalchemy import Vector 

if TYPE_CHECKING:
    from .file import File

class Chunk(Base):
    __tablename__ = "chunks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    text_content: Mapped[str] = mapped_column(
        Text, 
        nullable=False
    )

    start_line: Mapped[int] = mapped_column(nullable=False)
    end_line: Mapped[int] = mapped_column(nullable=False)

    class_name: Mapped[str | None] = mapped_column(
        nullable=True
    )

    func_name: Mapped[str | None] = mapped_column(
        nullable=True
    )

    #chunk_type = code or readme
    chunk_type: Mapped[str] = mapped_column(
        String, 
        nullable=False
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(768), # replace 768 with the embedding dimension required by the embedding model chosen
        nullable=False
    )

    metadata_ : Mapped[dict | None] = mapped_column(
        "metadata", # this is the actual PostgreSQL column name
        JSON, # column type in the database
        nullable=True
    )


    file_id: Mapped[int] = mapped_column(ForeignKey("files.id")) # file_id attribute must match with the "id" column from files table

    file: Mapped["File"] = relationship(back_populates="chunks")
    # Chunk.file <-> File.chunks 