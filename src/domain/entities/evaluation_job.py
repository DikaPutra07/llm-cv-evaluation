from datetime import datetime
from typing import Optional, Dict, Any, Literal

class EvaluationJob:
    """Entitas untuk melacak status proses AI screening."""
    
    STATUS_QUEUED: Literal["queued"] = "queued"
    STATUS_PROCESSING: Literal["processing"] = "processing"
    STATUS_COMPLETED: Literal["completed"] = "completed"
    STATUS_FAILED: Literal["failed"] = "failed"
    
    id: str
    cv_doc_id: str
    report_doc_id: str
    job_title: str
    status: str
    created_at: datetime
    updated_at: datetime
    # Result disimpan sebagai Dict sesuai format API
    result: Optional[Dict[str, Any]] = None 

    def __init__(self, id: str, cv_doc_id: str, report_doc_id: str, job_title: str):
        self.id = id
        self.cv_doc_id = cv_doc_id
        self.report_doc_id = report_doc_id
        self.job_title = job_title
        self.status = self.STATUS_QUEUED
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def set_processing(self):
        self.status = self.STATUS_PROCESSING
        self.updated_at = datetime.now()
        
    def set_completed(self, result_data: Dict[str, Any]):
        self.status = self.STATUS_COMPLETED
        self.result = result_data
        self.updated_at = datetime.now()

    def set_failed(self):
        self.status = self.STATUS_FAILED
        self.updated_at = datetime.now()
        
    def to_api_response(self) -> Dict[str, Any]:
        data = {
            "id": self.id,
            "status": self.status,
        }
        if self.status == self.STATUS_COMPLETED and self.result:
            data['result'] = self.result 
        
        return data