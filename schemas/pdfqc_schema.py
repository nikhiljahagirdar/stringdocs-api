from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from datetime import datetime


class PDFQCCreate(BaseModel):
    doc_id: int
    is_security: Optional[bool] = False
    is_encrypted: Optional[bool] = False
    has_bookmarks: Optional[bool] = False
    has_tags: Optional[bool] = False
    has_media: Optional[bool] = False
    has_images: Optional[bool] = False
    has_fonts: Optional[bool] = False
    has_tables: Optional[bool] = False
    has_links: Optional[bool] = False
    has_annotations: Optional[bool] = datetime.now().isoformat()
    has_form_fields: Optional[bool] = False
    createdon: Optional[datetime] = datetime.now().isoformat()
    updatedon: Optional[datetime] = None

    class config:
        from_attributes = True


class PDFQCRead(BaseModel):
    doc_id: int
    is_security: Optional[bool] = False
    is_encrypted: Optional[bool] = False
    has_bookmarks: Optional[bool] = False
    has_tags: Optional[bool] = False
    has_media: Optional[bool] = False
    has_images: Optional[bool] = False
    has_fonts: Optional[bool] = False
    has_tables: Optional[bool] = False
    has_links: Optional[bool] = False
    has_annotations: Optional[bool] = False
    has_form_fields: Optional[bool] = False
    createdon: Optional[datetime] = None
    updatedon: Optional[datetime] = None

    class config:
        from_attributes = True
