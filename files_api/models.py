from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class FileRecord(Base):
    __tablename__ = "file_records"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, index=True)
    directory = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)