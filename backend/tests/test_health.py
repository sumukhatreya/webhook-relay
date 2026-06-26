from unittest.mock import AsyncMock, patch

import httpx
import pytest

from app.main import app


@pytest.mark.asyncio
async def test_health_all_services_up():
    with (
        patch("app.api.routes.health.check_postgres", new_callable=AsyncMock) as pg,
        patch("app.api.routes.health.check_redis", new_callable=AsyncMock) as redis,
        patch("app.api.routes.health.check_rabbitmq", new_callable=AsyncMock) as rmq,
    ):
        pg.return_value = True
        redis.return_value = True
        rmq.return_value = True

        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.get("/health")

        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert data["services"] == {"postgres": "ok", "redis": "ok", "rabbitmq": "ok"}


@pytest.mark.asyncio
async def test_health_service_down():
    with (
        patch("app.api.routes.health.check_postgres", new_callable=AsyncMock) as pg,
        patch("app.api.routes.health.check_redis", new_callable=AsyncMock) as redis,
        patch("app.api.routes.health.check_rabbitmq", new_callable=AsyncMock) as rmq,
    ):
        pg.return_value = True
        redis.side_effect = ConnectionError("redis down")
        rmq.return_value = True

        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.get("/health")

        assert resp.status_code == 503
        data = resp.json()
        assert data["status"] == "degraded"
        assert data["services"]["postgres"] == "ok"
        assert data["services"]["redis"] == "unavailable"
        assert data["services"]["rabbitmq"] == "ok"
