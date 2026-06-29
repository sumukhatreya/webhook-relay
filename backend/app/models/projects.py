from app.core.db import Base
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
import uuid
import secrets


class Project(Base):
    __tablename__ = "projects"
    
    # --------------------------------- Columns -----------------------------------
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    hmac_signing_secret: Mapped[str] = mapped_column(
        nullable=False, default=lambda: secrets.token_hex(32)
    )
    org_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )

    # --------------------------------- Relationships --------------------------------
    org: Mapped["Organization"] = relationship(back_populates="projects")
    sources: Mapped[List["Source"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
