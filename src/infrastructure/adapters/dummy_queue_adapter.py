from src.domain.ports.queue_repository import IJobQueueService

class DummyJobQueueAdapter(IJobQueueService):
    """Adapter dummy untuk meniru Celery/Queue."""
    
    def enqueue_evaluation(self, job_id: str) -> None:
        print(f"[QUEUE LOG]: Job {job_id} successfully added to the DUMMY queue.")
        pass