from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "payment_aggregator",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.webhook_tasks", "app.tasks.payment_tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,
    task_soft_time_limit=240,
)
