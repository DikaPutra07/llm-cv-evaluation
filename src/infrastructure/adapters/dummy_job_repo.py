from src.domain.ports.evaluation_repository import IEvaluationJobRepository
from src.domain.entities.evaluation_job import EvaluationJob
from typing import Optional, Dict

class DummyEvaluationJobRepository(IEvaluationJobRepository):
    """DUMMY Repo buat simulasi Postgres Job Storage."""
    
    _db: Dict[str, EvaluationJob] = {}
    
    async def save(self, job: EvaluationJob) -> None:
        # 1. Simulate Long Running Process completion (Hanya untuk testing alur)
        if job.status == EvaluationJob.STATUS_QUEUED:
            # Di real app, ini gak ada. Worker yang akan set status ini.
            # Ini simulasi langsung COMPLETED biar /result bisa test completed state.
            job.set_completed(result={
                "cv_match_rate": 0.82,
                "cv_feedback": "Dummy: Strong in backend, limited AI exp.",
                "project_score": 4.5,
                "project_feedback": "Dummy: Meets chaining reqs, lacks error handling.",
                "overall_summary": "Dummy: Good candidate fit, would benefit from RAG knowledge."
            })
        
        self._db[job.id] = job
        print(f"[DUMMY JOB REPO]: Job {job.id} status updated to {job.status}.")

    async def get_by_id(self, job_id: str) -> Optional[EvaluationJob]:
        return self._db.get(job_id)