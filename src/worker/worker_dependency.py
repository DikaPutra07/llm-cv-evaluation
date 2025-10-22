# src/infrastructure/worker_deps.py
from typing import Dict, Any
from src.infrastructure.db_models import AsyncSessionLocal 
from src.infrastructure.adapters.document_adapters import DocumentAdapter
from src.infrastructure.adapters.job_adapter import PostgresEvaluationJobAdapter
from src.infrastructure.adapters.llm_adapter import LLMAdapter
from src.infrastructure.adapters.rag_adapter import MilvusRAGAdapter


job_repo = PostgresEvaluationJobAdapter(session_maker=AsyncSessionLocal) 
rag_service = MilvusRAGAdapter()
llm_service = LLMAdapter()
document_repo_instance = DocumentAdapter(session_maker=AsyncSessionLocal)

def resolve_worker_dependencies() -> Dict[str, Any]:
    """Mengumpulkan dependencies untuk digunakan oleh Celery Task."""
    return {
        "job_repo": job_repo,
        "document_repo": document_repo_instance,
        "rag_service": rag_service,
        "llm_service": llm_service,
    }