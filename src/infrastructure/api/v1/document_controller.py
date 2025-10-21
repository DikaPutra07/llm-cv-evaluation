import os
import uuid
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from src.application.use_cases.upload_document import UploadDocumentUseCase
from src.domain.entities.document import CandidateDocument, DocType
from src.infrastructure.di_container import get_upload_document_use_case 

router = APIRouter()

# Endpoint: POST /upload
@router.post("/upload", status_code=status.HTTP_201_CREATED, response_model=dict)
async def upload_documents(
    cv_file: UploadFile = File(..., description="Candidate CV (PDF)"),
    report_file: UploadFile = File(..., description="Project Report (PDF)"),
    upload_uc: UploadDocumentUseCase = Depends(get_upload_document_use_case) 
):
    UPLOAD_DIR = "/tmp/screening_uploads"
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    uploaded_docs: list[CandidateDocument] = []

    try:
        files_to_process = {
            'CV': cv_file, 
            'PROJECT_REPORT': report_file
        }
        
        for doc_type_str, file in files_to_process.items():
            doc_type: DocType = doc_type_str 
            
            unique_filename = f"{file.filename}-{uuid.uuid4().hex[:8]}.pdf"
            file_path = os.path.join(UPLOAD_DIR, unique_filename)
            
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
                
            doc: CandidateDocument = await upload_uc.execute(
                file_path=file_path, 
                file_name=file.filename, 
                doc_type=doc_type
            )
            uploaded_docs.append(doc)
            
        # 3. Kembalikan ID
        cv_id = [d.id for d in uploaded_docs if d.doc_type == 'CV'][0]
        report_id = [d.id for d in uploaded_docs if d.doc_type == 'PROJECT_REPORT'][0]
        
        return {
            "cv_id": cv_id,
            "report_id": report_id,
            "message": "Files stored, IDs returned for later processing."
        }
    
    except Exception as e:
        print(f"FATAL ERROR during upload: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail=f"Internal service error: {str(e)}")