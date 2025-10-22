from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.evaluation_job import EvaluationJob

class IEvaluationJobRepository(ABC):
    """Port untuk menyimpan dan mengelola status EvaluationJob."""

    @abstractmethod
    async def save(self, job: EvaluationJob) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, job_id: str) -> Optional[EvaluationJob]:
        pass