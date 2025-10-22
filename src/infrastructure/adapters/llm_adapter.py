import asyncio
from typing import Dict, Any, List
from src.domain.ports.queue_repository import ILLMService

class LLMAdapter(ILLMService):
    async def run_cv_evaluation(self, cv_text: str, context: List[str]) -> Dict[str, Any]:
        await asyncio.sleep(1) # Simulasi Latency
        return {"cv_match_rate": 0.82, "cv_feedback": "dummy."}
    async def run_project_evaluation(self, report_text: str, context: List[str]) -> Dict[str, Any]:
        await asyncio.sleep(1)
        return {"project_score": 4.5, "project_feedback": "dummy."}
    async def run_final_synthesis(self, cv_result: Dict, project_result: Dict) -> Dict[str, str]:
        await asyncio.sleep(1)
        return {"overall_summary": "dummy."}