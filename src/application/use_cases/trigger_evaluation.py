import uuid
from src.domain.entities.evaluation_job import EvaluationJob
from src.domain.ports.evaluation_repository import IEvaluationJobRepository 
from src.domain.ports.queue_repository import IJobQueueService

class TriggerEvaluationUseCase:
    """Logika untuk membuat job baru dan mengirimnya ke Queue."""
    
    def __init__(self, job_repo: IEvaluationJobRepository, queue_service: IJobQueueService):
        self.job_repo = job_repo
        self.queue_service = queue_service

    async def execute(self, job_title: str, cv_doc_id: str, report_doc_id: str) -> EvaluationJob:
        job_id = str(uuid.uuid4())
        
        job = EvaluationJob(
            id=job_id,
            job_title=job_title,
            cv_doc_id=cv_doc_id,
            report_doc_id=report_doc_id
        )
        
        await self.job_repo.save(job)
        
        self.queue_service.enqueue_evaluation(job_id=job.id)
        
        return job