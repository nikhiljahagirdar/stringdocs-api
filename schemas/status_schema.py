from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from datetime import datetime


class SiteStatusCreate(BaseModel):
    """
    Pydantic model for creating a new site status entry.
    """

    status_type: str
    status_message: str
    pdf_file_id: Optional[int] = None
    createdon: Optional[datetime] = datetime.now().isoformat()
    updatedon: Optional[datetime] = None

    class Config:
        from_attributes = True


class SiteStatusRead(BaseModel):
    """
    Pydantic model representing the 'sitestatus' table.
    """

    id: Optional[int] = None
    status_type: str
    status_message: str
    pdf_file_id: Optional[int] = None
    createdon: Optional[datetime] = None
    updatedon: Optional[datetime] = None

    class Config:
        from_attributes = True
