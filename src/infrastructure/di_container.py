from fastapi import Depends
from src.application.use_cases.upload_document import UploadDocumentUseCase
from src.infrastructure.adapters.document_adapters import DocumentAdapter
from src.infrastructure.db_models import AsyncSessionLocal 

document_repo_instance = DocumentAdapter(
    session_maker=AsyncSessionLocal
)

upload_document_uc_instance = UploadDocumentUseCase(
    document_repo=document_repo_instance
)

# --- Dependency Function buat FastAPI ---

def get_upload_document_use_case() -> UploadDocumentUseCase:
    return upload_document_uc_instance