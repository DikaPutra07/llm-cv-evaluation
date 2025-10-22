from datetime import datetime
from typing import Literal, Dict, Any

DocType = Literal['CV', 'PROJECT_REPORT']

class CandidateDocument:
    """Entitas buat CV atau Project Report."""
    
    id: str
    file_path: str 
    file_name: str
    doc_type: DocType
    created_at: datetime

    def __init__(self, id: str, file_path: str, file_name: str, doc_type: DocType, created_at: datetime = None):
        self.id = id
        self.file_path = file_path
        self.file_name = file_name
        self.doc_type = doc_type
        if created_at is None:
            self.created_at = datetime.now()
        else:
            self.created_at = created_at