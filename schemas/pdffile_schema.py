from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from datetime import datetime


class PDFFileCreate(BaseModel):
    user_id: Optional[int]
    filename: str
    path: str
    size: int
    original_filename: str
    processed_filename: Optional[str] = None
    processed_path: Optional[str] = None
    processing_start_time: Optional[datetime] = None
    processing_end_time: Optional[datetime] = None
    status: Optional[str] = ""
    status_message: Optional[str] = ""
    createdon: Optional[datetime] = datetime.now().isoformat()
    updatedon: Optional[datetime] = None

    class Config:
        from_attributes = True


class PDFFileRead(BaseModel):
    id: int
    user_id: Optional[int]
    filename: str
    path: str
    size: int
    original_filename: str
    processed_filename: Optional[str] = None
    processed_path: Optional[str] = None
    processing_start_time: Optional[datetime] = None
    processing_end_time: Optional[datetime] = None
    status: Optional[str] = ""
    status_message: Optional[str] = ""
    createdon: Optional[datetime] = None
    updatedon: Optional[datetime] = None

    class Config:
        from_attributes = True
