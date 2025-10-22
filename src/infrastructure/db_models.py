from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, DateTime
from fastapi import Depends
import os
from dotenv import load_dotenv
from sqlalchemy.pool import NullPool

load_dotenv()

Base = declarative_base()
DATABASE_URL = os.getenv("DATABASE_URL")

# --- DB Model ---
class DocumentModel(Base):
    __tablename__ = 'documents'

    id = Column(String, primary_key=True, index=True)
    file_path = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    doc_type = Column(String, nullable=False) 
    created_at = Column(DateTime, nullable=False)

class EvaluationJobModel(Base): # BARU
    __tablename__ = 'evaluation_jobs'
    id = Column(String, primary_key=True, index=True)
    cv_doc_id = Column(String, nullable=False)
    report_doc_id = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    result = Column(String, nullable=True)
    

async_engine = create_async_engine(
    DATABASE_URL, 
    echo=False, 
    future=True,
    pool_size=30
)

AsyncSessionLocal = sessionmaker(
    async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("INFO: Database tables created/checked.")