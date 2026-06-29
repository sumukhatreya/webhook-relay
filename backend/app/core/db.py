from sqlalchemy import create_engine, DateTime, func
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column
from app.core.config import settings
from datetime import datetime


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


# --- Async side: used by FastAPI request handlers ---
async_engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_db():
    """FastAPI dependency."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# --- Sync side: used by Celery tasks and Alembic ---
sync_engine = create_engine(settings.DATABASE_URL_SYNC, pool_pre_ping=True)
SyncSessionLocal = sessionmaker(sync_engine, expire_on_commit=False)
