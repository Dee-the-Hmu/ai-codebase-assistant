from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime

from .base import Base
from datetime import datetime, timezone

from typing import TYPE_CHECKING

if TYPE_CHECKING: 
    from .repository import Repository # VS Code understands that: repository: Mapped["Repository"] refers to your Repository class, even though that import does not run when the application starts.
    from .chunk import Chunk

class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    path: Mapped[str] = mapped_column(
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        nullable=False
    )

    size_bytes: Mapped[int | None] = mapped_column(
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    repo_id: Mapped[int] = mapped_column(ForeignKey("repositories.id")) #repo_id attribute must match with the "id" column in the "repositories table"

    repository: Mapped["Repository"] = relationship(back_populates="files")
    """
    repository = will hold 1 related Repository object 
    backpopulate="files"
        points the attribute named "files" inside the Repository class 

    connecting: Repository.files  ↔  File.repository
    """

    chunks: Mapped[list["Chunk"]] = relationship(back_populates="file")
    # File.chunks <-> Chunk.file