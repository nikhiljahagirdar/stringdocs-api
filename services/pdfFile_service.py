from core.db.asynccrud import (
    select_all,
    select_where,
    select_where_single,
    insert,
    update,
    delete,
    custom_query_one,
)
from schemas.pdffile_schema import PDFFileCreate, PDFFileRead
from typing import Optional, List
from datetime import datetime
import logging
from fastapi.responses import StreamingResponse

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class PDFFileService:
    async def create_pdf_file(self, data: PDFFileCreate) -> Optional[PDFFileRead]:
        pdf_files = []
        try:
            result = await insert("pdffile", data.model_dump())
            return PDFFileRead(**result) if result else None
        except Exception as e:
            logging.error(f"Error creating PDF file: {e}")
            raise

    async def get_all_pdf_files(self) -> List[PDFFileRead]:
        try:
            logger.info("Getting all PDF files")
            rows = await select_all("public.pdffile")
            logger.info(rows)
            return [PDFFileRead(**row) for row in rows]
        except Exception as e:
            logging.error(f"Error getting all PDF files: {e}")
            raise

    async def get_pdf_file(self, file_id: int) -> Optional[PDFFileRead]:
        try:
            row = await select_where_single("pdffile", "id=%s", (file_id,))
            return PDFFileRead(**row) if row else None
        except Exception as e:
            logging.error(f"Error getting PDF file: {e}")
            raise

    async def delete_pdf_file(self, file_id: int) -> Optional[PDFFileRead]:
        try:
            row = await delete("pdffile", "id=%s", (file_id,))
            return PDFFileRead(**row) if row else None
        except Exception as e:
            logging.error(f"Error deleting PDF file: {e}")
            raise

    async def update_pdf_file_status(self, file_id: int, status: str):
        try:
            await update("pdffile", {"status": status}, "id=%s", (file_id,))
        except Exception as e:
            logging.error(f"Error updating PDF file status: {e}")
            raise

