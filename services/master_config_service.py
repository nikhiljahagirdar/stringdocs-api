from core.db.asynccrud import (
    select_all,
    select_where,
    select_where_single,
    insert,
    update,
    delete,
    custom_query_one,
)
from schemas.master_config_schema import PdfMasterConfigCreate, PdfMasterConfigRead
from typing import Optional, List
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class PdfMasterConfigService:
    async def create_pdf_master_config(
        self, config: PdfMasterConfigCreate
    ) -> Optional[PdfMasterConfigRead]:
        try:
            result = await insert("pdfMasterConfig", config.model_dump())
            if result:
                return PdfMasterConfigRead(**result)
            return None
        except Exception as e:
            logging.error(f"Error creating PDF master config: {e}")
            raise

    async def get_pdf_master_config(
        self, config_id: int
    ) -> Optional[PdfMasterConfigRead]:
        """
        Retrieves a PDF master config entry by its ID.
        """
        try:
            result = await select_where_single(
                "pdfmasterconfig", "id = %s", (config_id,)
            )
            if result:
                return PdfMasterConfigRead(**result)
            return None
        except Exception as e:
            logging.error(f"Error getting PDF master config: {e}")
            raise

    async def get_all_pdf_master_configs(self) -> List[PdfMasterConfigRead]:
        """
        Retrieves all PDF master config entries.
        """
        try:
            results = await select_all("pdfmasterconfig")
            return [PdfMasterConfigRead(**row) for row in results]
        except Exception as e:
            logging.error(f"Error getting all PDF master configs: {e}")
            raise

    async def update_pdf_master_config(
        self, config_id: int, config: PdfMasterConfigCreate
    ) -> Optional[PdfMasterConfigRead]:
        """
        Updates an existing PDF master config entry.
        """
        try:
            result = await update(
                "pdfmasterconfig", config.dict(), "id = %s", (config_id,)
            )
            if result:
                return PdfMasterConfigRead(**result)
            return None
        except Exception as e:
            logging.error(f"Error updating PDF master config: {e}")
            raise

    async def delete_pdf_master_config(self, config_id: int) -> bool:
        """
        Deletes a PDF master config entry by its ID.
        """
        try:
            result = await delete("pdfmasterconfig", "id=%s", (config_id,))
            return result is not None
        except Exception as e:
            logging.error(f"Error deleting PDF master config: {e}")
            raise
