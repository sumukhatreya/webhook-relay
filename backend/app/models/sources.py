from app.core.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy import String, ForeignKey
from typing import List
import uuid


class Source(Base):
    __tablename__ = "sources"

    # --------------------------------- Columns -----------------------------------
    id: Mapped[str] = mapped_column(
        primary_key=True, default=lambda: f"src_{uuid.uuid4().hex}"
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE")
    )
    allowed_methods: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=False)
    auth: Mapped[bool] = mapped_column(default=False)
    auth_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    auth_config: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    # --------------------------------- Relationships ------------------------------
    project: Mapped["Project"] = relationship(back_populates="sources")
