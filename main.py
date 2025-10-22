from fastapi import FastAPI
from src.infrastructure.api.v1 import document_controller
from src.infrastructure.api.v1 import evaluation_controller
from src.infrastructure.db_models import init_db 

app = FastAPI(title="AI Screening Backend Service")

@app.on_event("startup")
async def startup_event():
    await init_db() 

prefix = "/api/v1"

app.include_router(document_controller.router, tags=["Documents"], prefix=prefix)
app.include_router(evaluation_controller.router, tags=["Evaluation"], prefix=prefix)

@app.get("/")
def read_root():
    return {"message": "AI Screening Service is running"}