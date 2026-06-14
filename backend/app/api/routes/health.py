from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health() -> dict:
    # TODO: ping Postgres (SELECT 1), Redis (PING), RabbitMQ (connection check)
    # and return 503 if any are down — per your design doc.
    return {"status": "ok"}