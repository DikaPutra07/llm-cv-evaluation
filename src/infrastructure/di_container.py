from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
from src.infrastructure.db_models import AsyncSessionLocal 
from src.infrastructure.adapters.document_adapters import DocumentAdapter
from src.infrastructure.adapters.job_adapter import PostgresEvaluationJobAdapter # Real Job Repo
from src.application.use_cases.upload_document import UploadDocumentUseCase
from src.application.use_cases.trigger_evaluation import TriggerEvaluationUseCase
from src.infrastructure.adapters.queue_adapter import CeleryJobQueueAdapter 
from src.infrastructure.adapters.llm_adapter import LLMAdapter     
from src.infrastructure.adapters.rag_adapter import MilvusRAGAdapter
from typing import Dict

document_repo_instance = DocumentAdapter(
    session_maker=AsyncSessionLocal
)

upload_document_uc_instance = UploadDocumentUseCase(
    document_repo=document_repo_instance
)

# --- CORE SINGLETON INSTANCES ---
job_repo_instance = PostgresEvaluationJobAdapter(session_maker=AsyncSessionLocal) # REAL DB ADAPTER
queue_service_instance = CeleryJobQueueAdapter()            
rag_service_instance = MilvusRAGAdapter()                   
llm_service_instance = LLMAdapter()                 

trigger_evaluation_uc_instance = TriggerEvaluationUseCase(
    job_repo=job_repo_instance,
    queue_service=queue_service_instance
)


def get_upload_document_use_case() -> UploadDocumentUseCase:
    return upload_document_uc_instance

def get_trigger_evaluation_use_case() -> TriggerEvaluationUseCase:
    return trigger_evaluation_uc_instance