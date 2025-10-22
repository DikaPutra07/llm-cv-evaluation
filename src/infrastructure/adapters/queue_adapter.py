from src.domain.ports.queue_repository import IJobQueueService
from src.worker.tasks import run_evaluation_task

class CeleryJobQueueAdapter(IJobQueueService):
    def enqueue_evaluation(self, job_id: str) -> None:
        run_evaluation_task.apply_async(args=[job_id]) 
        print(f"[CELERY LOG]: Job {job_id} delegated to Celery worker.")