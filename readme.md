# Webhook Relay

A self-hosted webhook delivery service that guarantees at-least-once delivery from incoming sources to configured destinations. Supports filtering, deduplication, rate limiting, automatic retries with exponential backoff, and manual replay of failed events via a dead letter queue.

## Architecture

```
Sources → FastAPI → Ingestion Queue → Routing Worker → Delivery Queue → Delivery Worker → Destinations
                                                                              ↓ (on failure)
                                                                         Retry Queue → Dead Letter Queue
```

- **FastAPI** — ingestion endpoint with HMAC/API key auth, plus a management API for CRUD on sources, destinations, and connections
- **PostgreSQL** — primary data store
- **RabbitMQ** — message broker (ingestion and delivery queues)
- **Celery** — two worker pools (routing and delivery), prefork mode with 4 workers each
- **Redis** — caching (source/connection config) and sliding window rate limiting
- **Flower** — Celery task monitoring dashboard

## Prerequisites

- Docker and Docker Compose

## Getting Started

```bash
# Clone and start all services
git clone <repo-url> && cd webhook-relay
docker compose up --build
```

| Service         | URL                        |
| --------------- | -------------------------- |
| API             | http://localhost:8000      |
| Health check    | http://localhost:8000/health |
| RabbitMQ UI     | http://localhost:15672 (guest/guest) |
| Flower          | http://localhost:5555      |

## Development

The backend uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
cd backend
uv sync            # install dependencies
uv run pytest      # run tests
uv run ruff check . # lint
uv run ruff format --check . # format check
```

Database migrations are managed with Alembic:

```bash
uv run alembic upgrade head
```

## Configuration

Copy the example env file and adjust as needed:

```bash
cp backend/.env.example backend/.env
```

| Variable           | Description                      |
| ------------------ | -------------------------------- |
| `DATABASE_URL`     | Async PostgreSQL connection string |
| `DATABASE_URL_SYNC`| Sync PostgreSQL connection string (for Alembic/Celery) |
| `REDIS_URL`        | Redis connection string          |
| `RABBITMQ_URL`     | RabbitMQ AMQP connection string  |
| `DEBUG`            | Enable debug logging             |

## API Overview

- `POST /webhooks/:source_id` — ingest a webhook (max 1MB payload)
- `GET /health` — dependency health check (Postgres, Redis, RabbitMQ)
- CRUD endpoints for `/projects`, `/sources`, `/destinations`, `/connections`
- `GET /requests`, `GET /events` — inspect ingested data and delivery status
- `POST /events/:event_id/replay` — manually retry a failed event

See [design.md](design.md) for the full API reference, data model, failure modes, and caching strategy.
