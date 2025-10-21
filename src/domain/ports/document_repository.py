from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.document import CandidateDocument

# Interface Document Repository

class IDocumentRepository(ABC):

    @abstractmethod
    async def save(self, document: CandidateDocument) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, doc_id: str) -> Optional[CandidateDocument]:
        pass