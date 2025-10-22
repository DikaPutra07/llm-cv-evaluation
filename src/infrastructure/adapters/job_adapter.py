import json
from typing import Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.domain.ports.evaluation_repository import IEvaluationJobRepository 
from src.domain.entities.evaluation_job import EvaluationJob
from src.infrastructure.db_models import EvaluationJobModel

class PostgresEvaluationJobAdapter(IEvaluationJobRepository):
    def __init__(self, session_maker: Any): self.session_maker = session_maker
    async def save(self, job: EvaluationJob) -> None:
        async with self.session_maker() as session:
            session: AsyncSession
            
            stmt = select(EvaluationJobModel).where(EvaluationJobModel.id == job.id)
            existing_model = await session.scalar(stmt)
            
            result_json = json.dumps(job.result) if job.result else None
            
            if existing_model:
                # Update
                existing_model.status = job.status
                existing_model.updated_at = job.updated_at
                existing_model.result = result_json
            else:
                # Insert
                db_model = EvaluationJobModel(
                    id=job.id, cv_doc_id=job.cv_doc_id, report_doc_id=job.report_doc_id, 
                    job_title=job.job_title, status=job.status, created_at=job.created_at, 
                    updated_at=job.updated_at, result=result_json
                )
                session.add(db_model)
            
            await session.commit()
            print(f"[DB LOG]: Job {job.id} status set to {job.status} in REAL DB.")

    async def get_by_id(self, job_id: str) -> Optional[EvaluationJob]:
        async with self.session_maker() as session:
            session: AsyncSession
            stmt = select(EvaluationJobModel).where(EvaluationJobModel.id == job_id)
            db_model = await session.scalar(stmt)
            if db_model:
                result_data = json.loads(db_model.result) if db_model.result else None
                job = EvaluationJob(id=db_model.id, cv_doc_id=db_model.cv_doc_id, report_doc_id=db_model.report_doc_id, job_title=db_model.job_title)
                job.status = db_model.status
                job.created_at = db_model.created_at
                job.updated_at = db_model.updated_at
                job.result = result_data
                return job
            return None