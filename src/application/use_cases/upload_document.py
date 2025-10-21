import uuid
from src.domain.entities.document import CandidateDocument, DocType
from src.domain.ports.document_repository import IDocumentRepository

class UploadDocumentUseCase:
    """Logika inti untuk proses upload dan penyimpanan metadata."""
    
    def __init__(self, document_repo: IDocumentRepository):
        self.document_repo = document_repo

    async def execute(self, file_path: str, file_name: str, doc_type: DocType) -> CandidateDocument:
        doc_id = str(uuid.uuid4())

        document = CandidateDocument(
            id=doc_id,
            file_path=file_path,  
            file_name=file_name, 
            doc_type=doc_type
        )
        
        await self.document_repo.save(document)
        
        return document