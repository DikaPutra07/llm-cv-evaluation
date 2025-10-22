from celery import Celery
import os
# Ganti localhost dengan nama service Docker (kalau pake docker-compose)
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0") 
CELERY_BACKEND_URL = os.getenv("CELERY_BACKEND_URL", "redis://localhost:6379/1")

celery_app = Celery(
    "evaluation_tasks", 
    broker=CELERY_BROKER_URL, 
    backend=CELERY_BACKEND_URL,
    include=["src.worker.tasks"]
)
celery_app.conf.update(
    task_track_started=False,
    task_serializer='json', 
    result_serializer='json', 
    accept_content=['json'], 
    timezone='Asia/Jakarta', 
    enable_utc=True
)