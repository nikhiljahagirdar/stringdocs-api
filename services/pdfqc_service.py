from core.db.asynccrud import (
    select_all,
    select_where,
    select_where_single,
    insert,
    update,
    delete,
    custom_query_one,
)
from schemas.pdfqc_schema import PDFQCCreate, PDFQCRead
from typing import Optional, List
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class PDFQCService:
    async def create_pdf_qc(self, data: PDFQCCreate) -> Optional[PDFQCRead]:
        try:
            result = await insert("pdfqc", data.model_dump())
            return PDFQCRead(**result) if result else None
        except Exception as e:
            logging.error(f"Error creating PDF QC: {e}")
            raise

    async def get_all_pdf_qc(self) -> List[PDFQCRead]:
        try:
            rows = await select_all("pdfqc")
            return [PDFQCRead(**row) for row in rows]
        except Exception as e:
            logging.error(f"Error getting all PDF QCs: {e}")
            raise

    async def get_pdf_qc(self, qc_id: int) -> Optional[PDFQCRead]:
        try:
            row = await select_where_single("pdfqc", "id=%s", (qc_id,))
            return PDFQCRead(**row) if row else None
        except Exception as e:
            logging.error(f"Error getting PDF QC: {e}")
            raise

    async def delete_pdf_qc(self, qc_id: int) -> Optional[PDFQCRead]:
        try:
            row = await delete("pdfqc", "id=%s", (qc_id,))
            return PDFQCRead(**row) if row else None
        except Exception as e:
            logging.error(f"Error deleting PDF QC: {e}")
            raise
        
    async def get_qc_by_file(self, file_id: int) -> Optional[PDFQCRead]:
        try:
            row = await custom_query_one(
                "SELECT * FROM pdfqc WHERE doc_id = %s", (file_id,)
            )
            return PDFQCRead(**row) if row else None
        except Exception as e:
            logging.error(f"Error deleting PDF QC: {e}")
            raise    
