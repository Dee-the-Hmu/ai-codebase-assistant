from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from datetime import datetime, timezone

from sqlalchemy import DateTime

from typing import TYPE_CHECKING

if TYPE_CHECKING: 
    from .file import File
    
class Repository(Base):
    __tablename__ = "repositories"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    github_url: Mapped[str] = mapped_column(
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        nullable=False
    )

    owner: Mapped[str] = mapped_column(
        nullable=False
    )

    default_branch: Mapped[str] = mapped_column(
        nullable=False
    )

    latest_commit_sha: Mapped[str | None] = mapped_column( # the unique Git commit identifier for the most recently ingested commit 
        nullable=True
    )

    ingestion_status: Mapped[str] = mapped_column(
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default= lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )


    files: Mapped[list["File"]] = relationship(back_populates="repository")  #files = a list of "File" objects
    """
    files = a list of "File" objects
    1 repository can have many files 
    back_populate="repository" 
        points to the attribute named "repository" inside the File class

    SQLAlchemy connects these 2 attributes: Repository.files  ↔  File.repository

    actual database connection come from repo_id: Mapped[int] = mapped_column(ForeignKey("repositories.id"))
    """
