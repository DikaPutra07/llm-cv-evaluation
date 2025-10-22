import asyncio
from src.worker.celery_app import celery_app
from src.application.workers.evaluation_pipeline import EvaluationPipeline
from src.worker.worker_dependency import resolve_worker_dependencies

@celery_app.task(bind=True)
def run_evaluation_task(self, job_id: str):
    """Task Celery yang menjalankan Master Pipeline."""
    
    deps = resolve_worker_dependencies()
    
    pipeline = EvaluationPipeline(
        job_repo=deps['job_repo'],
        document_repo=deps['document_repo'],
        rag_service=deps['rag_service'],
        llm_service=deps['llm_service']
    )
    

    try:
        asyncio.run(pipeline.execute(job_id))       
        return "Evaluation pipeline completed successfully"
        
    except Exception as e:
        raise self.retry(exc=e, countdown=60, max_retries=3)



