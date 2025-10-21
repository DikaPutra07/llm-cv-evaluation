from fastapi import FastAPI
from src.infrastructure.api.v1 import document_controller
from src.infrastructure.db_models import init_db 

app = FastAPI(title="AI Screening Backend Service")

# Setup Event Startup
@app.on_event("startup")
async def startup_event():
    # Ini akan membuat table 'documents' di Postgres Docker lo
    await init_db() 

# Register Router
app.include_router(document_controller.router, tags=["Documents"], prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "AI Screening Service is running"}