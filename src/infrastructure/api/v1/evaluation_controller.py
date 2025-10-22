from fastapi import APIRouter, Depends, status, Form
from pydantic import BaseModel
from src.application.use_cases.trigger_evaluation import TriggerEvaluationUseCase
from src.infrastructure.di_container import get_trigger_evaluation_use_case 

router = APIRouter()

class EvaluateRequest(BaseModel):
    job_title: str
    cv_id: str
    report_id: str

# Endpoint: POST /evaluate
@router.post("/evaluate", status_code=status.HTTP_202_ACCEPTED, response_model=dict)
async def evaluate_application(
    job_title: str = Form(..., description="Job Title"),
    cv_id: str = Form(..., description="Candidate CV Document ID"),
    report_id: str = Form(..., description="Project Report Document ID"),
    trigger_uc: TriggerEvaluationUseCase = Depends(get_trigger_evaluation_use_case)
):
    job = await trigger_uc.execute(
        job_title=job_title,
        cv_doc_id=cv_id,
        report_doc_id=report_id
    )
    # Langsung return Job ID dan status: queued
    return job.to_api_response()