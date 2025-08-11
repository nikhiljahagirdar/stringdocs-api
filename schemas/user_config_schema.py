from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PdfUserConfigCreate(BaseModel):
    config_id: int
    user_id: int
    doc_id: int

    class config:
        from_attributes = True


class PdfUserConfigRead(BaseModel):
    id: int
    config_id: int
    user_id: int
    doc_id: int
    createdon: Optional[datetime] = None
    updatedon: Optional[datetime] = None

    class config:
        from_attributes = True
