from typing import Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.domain.ports.document_repository import IDocumentRepository 
from src.domain.entities.document import CandidateDocument 
from src.infrastructure.db_models import DocumentModel

class DocumentAdapter(IDocumentRepository):
    
    def __init__(self, session_maker: Any):
        self.session_maker = session_maker

    async def save(self, document: CandidateDocument) -> None:
        async with self.session_maker() as session:
            session: AsyncSession
            
            db_model = DocumentModel(
                id=document.id,
                file_path=document.file_path,
                file_name=document.file_name,
                doc_type=document.doc_type,
                created_at=document.created_at
            )
            
            session.add(db_model)
            await session.commit()
            print(f"LOG: Stored Document ID: {document.id} successfully.")

    async def get_by_id(self, doc_id: str) -> Optional[CandidateDocument]:
        async with self.session_maker() as session:
            session: AsyncSession
            
            stmt = select(DocumentModel).where(DocumentModel.id == doc_id)
            result = await session.execute(stmt)
            db_model = result.scalar_one_or_none()
            
            if db_model:
                return CandidateDocument(
                    id=db_model.id,
                    file_path=db_model.file_path,
                    file_name=db_model.file_name,
                    doc_type=db_model.doc_type,
                    created_at=db_model.created_at
                )
            
            return None