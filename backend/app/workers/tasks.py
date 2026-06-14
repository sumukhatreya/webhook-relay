from app.workers.celery_app import celery_app


@celery_app.task(name="ingestion.route_request")
def route_request(request_id: str) -> None:
    # TODO: load request, look up connections, evaluate rules,
    # create events, enqueue deliver_event per event.
    print(f"[routing] processing request {request_id}")
    deliver_event.delay(event_id=f"evt_for_{request_id}")


@celery_app.task(name="delivery.deliver_event", bind=True, max_retries=5)
def deliver_event(self, event_id: str) -> None:
    # TODO: load event, HTTP POST to destination, log attempt,
    # retry with backoff on failure, dead-letter when exhausted.
    print(f"[delivery] delivering event {event_id}")
