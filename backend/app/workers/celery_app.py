from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "webhook_relay",
    broker=settings.RABBITMQ_URL,
    backend=None,
    include=["app.workers.tasks"],
)

celery_app.conf.update(
    # --- at-least-once delivery semantics (core to your design) ---
    task_acks_late=True,               # ack AFTER the task completes
    task_reject_on_worker_lost=True,   # requeue if the worker process dies mid-task
    worker_prefetch_multiplier=1,      # don't hoard messages in a busy worker

    # --- queue topology ---
    task_routes={
        "ingestion.route_request": {"queue": "ingestion"},
        "delivery.deliver_event": {"queue": "delivery"},
    },
    task_default_queue="ingestion",
)