from typing import Dict, List
from src.domain.ports.queue_repository import IRAGService

class MilvusRAGAdapter(IRAGService):
    async def retrieve_context(self, query: str, filters: Dict = None) -> List[str]:
        print(f"[RAG DUMMY]: Retrieving context for query: {query}")
        return ["Job Requirement: Technical Skills Match (Weight: 40%)", "Case Study Requirement: Correctness (Prompt & Chaining) (Weight: 30%)"]