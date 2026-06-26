import asyncio
from typing import Annotated
from urllib.parse import urlparse

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_db

router = APIRouter()


async def check_postgres(db: AsyncSession) -> bool:
    result = await db.execute(text("SELECT 1"))
    result.scalar()
    return True


async def check_redis() -> bool:
    r = Redis.from_url(settings.REDIS_URL)
    try:
        return await r.ping()
    finally:
        await r.aclose()


async def check_rabbitmq() -> bool:
    parsed = urlparse(settings.RABBITMQ_URL)
    host = parsed.hostname or "localhost"
    port = parsed.port or 5672
    _, writer = await asyncio.open_connection(host, port)
    writer.close()
    await writer.wait_closed()
    return True


@router.get(
    "/health",
    responses={503: {"description": "One or more services are unreachable"}},
)
async def health(db: Annotated[AsyncSession, Depends(get_db)]):
    checks = {}
    healthy = True

    for name, coro in [
        ("postgres", check_postgres(db)),
        ("redis", check_redis()),
        ("rabbitmq", check_rabbitmq()),
    ]:
        try:
            await coro
            checks[name] = "ok"
        except Exception:
            checks[name] = "unavailable"
            healthy = False

    status_code = status.HTTP_200_OK if healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    return JSONResponse(
        content={"status": "healthy" if healthy else "degraded", "services": checks},
        status_code=status_code,
    )
