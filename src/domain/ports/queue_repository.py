from abc import ABC, abstractmethod
from typing import Dict, Any, List

class IJobQueueService(ABC):
    """Port: Mengirim task ke background worker."""
    @abstractmethod
    def enqueue_evaluation(self, job_id: str) -> None:
        pass

class ILLMService(ABC):
    """Port: Berinteraksi dengan DeepSeek/LLM API."""
    @abstractmethod
    async def run_cv_evaluation(self, cv_text: str, context: List[str]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def run_project_evaluation(self, report_text: str, context: List[str]) -> Dict[str, Any]:
        pass
        

class IRAGService(ABC):
    """Port: Berinteraksi dengan Vector Database (Milvus)."""
    @abstractmethod
    async def retrieve_context(self, query: str, filters: Dict = None) -> List[str]:
        pass