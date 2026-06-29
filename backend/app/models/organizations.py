from app.core.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import List
import uuid


class Organization(Base):
    __tablename__ = "organizations"
    
    # --------------------------------- Columns -----------------------------------
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    # --------------------------------- Relationships -------------------------------
    projects: Mapped[List["Project"]] = relationship(
        back_populates="org", cascade="all, delete-orphan"
    )
