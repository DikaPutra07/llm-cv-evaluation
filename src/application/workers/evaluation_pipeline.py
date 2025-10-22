import asyncio
from typing import Dict, Any
from src.domain.entities.evaluation_job import EvaluationJob
from src.domain.ports.evaluation_repository import IEvaluationJobRepository
from src.domain.ports.document_repository import IDocumentRepository
from src.domain.ports.queue_repository import IRAGService, ILLMService

class EvaluationPipeline:
    """MASTER USE CASE: Menjalankan full AI Chaining Pipeline di background."""
    
    def __init__(self, job_repo: IEvaluationJobRepository, document_repo: IDocumentRepository, rag_service: IRAGService, llm_service: ILLMService):
        self.job_repo = job_repo
        self.document_repo = document_repo
        self.rag_service = rag_service
        self.llm_service = llm_service

    async def execute(self, job_id: str) -> None:
        # 0. Ambil Job dari DB dan set status 'processing'
        job: EvaluationJob = await self.job_repo.get_by_id(job_id)
        if not job:
            print(f"Job ID {job_id} not found.")
            return
        
        try:
            job.set_processing()
            await self.job_repo.save(job)
            
            cv_doc = await self.document_repo.get_by_id(job.cv_doc_id)
            report_doc = await self.document_repo.get_by_id(job.report_doc_id)

            cv_text = f"Content of CV for {job.job_title}..." 
            report_text = f"Content of Project Report for {job.job_title}..."
            await asyncio.sleep(2) # test delay

            context_cv = await self.rag_service.retrieve_context(query=job.job_title + " requirements", filters={'doc_type': 'JOB_DESC'})
            cv_result = await self.llm_service.run_cv_evaluation(cv_text=cv_text, context=context_cv)
            await asyncio.sleep(2) # test delay

            context_proj = await self.rag_service.retrieve_context(query='case study requirements', filters={'doc_type': 'CASE_STUDY'})
            project_result = await self.llm_service.run_project_evaluation(report_text=report_text, context=context_proj)
            await asyncio.sleep(2) # test delay
            
            final_summary = await self.llm_service.run_final_synthesis(cv_result, project_result)
            
            final_result: Dict[str, Any] = {
                **cv_result,
                **project_result,
                "overall_summary": final_summary.get('overall_summary')
            }
            
            job.set_completed(result_data=final_result)
            await self.job_repo.save(job)
            print(f"\n[PIPELINE SUCCESS]: Job {job_id} COMPLETED. Overall Summary: {final_summary.get('overall_summary')[:30]}...")

        except Exception as e:
            print(f"\n[PIPELINE FAILED]: Job {job_id} failed with error: {e}")
            job.set_failed()
            await self.job_repo.save(job)
            raise e