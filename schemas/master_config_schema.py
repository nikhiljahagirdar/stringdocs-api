# schemas/pdf_master_config_schema.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PdfMasterConfigCreate(BaseModel):
    configtype: str
    configname: str
    configvalue: str
    configDescription: Optional[str] = None
    isChild: Optional[bool] = False
    createdon: Optional[datetime] = datetime.now().isoformat()
    updatedon: Optional[datetime] = datetime.now().isoformat()

    class Config:
        from_attributes = True


class PdfMasterConfigRead(BaseModel):
    id: int
    configtype: str
    configname: str
    configvalue: str
    configDescription: Optional[str] = None
    isChild: Optional[bool] = False
    createdon: Optional[datetime] = datetime.now().isoformat()
    updatedon: Optional[datetime] = datetime.now().isoformat()

    class Config:
        from_attributes = True
