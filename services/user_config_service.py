from core.db.asynccrud import (
    select_all,
    select_where_single,
    select_where,
    insert,
    update,
    delete,
    custom_query_one
)
import logging
from typing import Optional, List
from datetime import datetime, timezone
from schemas.user_config_schema import PdfUserConfigCreate, PdfUserConfigRead


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class PdfUserConfigService:
    async def create_pdf_user_config(
        self, config: PdfUserConfigCreate
    ) -> Optional[PdfUserConfigRead]:
        query = """
            INSERT INTO pdfUserConfig (
                config_id, user_id, doc_id
            ) VALUES (%s, %s, %s)
            RETURNING *
        """
        values = (config.config_id, config.user_id, config.doc_id,)
        try:
            result = await custom_query_one(query=query, params=values)
            if result:
                return PdfUserConfigRead(**result)
            return None
        except Exception as e:
            logging.error(f"Error creating PDF user config: {e}")
            raise

    async def get_pdf_user_config(self, config_id: int) -> Optional[PdfUserConfigRead]:
        query = "SELECT * FROM pdfUserConfig WHERE id = %s"
        try:
            result = await select_where_single(query, (config_id,))
            if result:
                return PdfUserConfigRead(**result)
            return None
        except Exception as e:
            logging.error(f"Error retrieving PDF user config: {e}")
            raise

    async def get_all_pdf_user_configs(self) -> List[PdfUserConfigRead]:
        query = "SELECT * FROM pdfUserConfig"
        try:
            results = await select_all("pdfUserConfig")
            return [PdfUserConfigRead(**row) for row in results]
        except Exception as e:
            logging.error(f"Error fetching all PDF user configs: {e}")
            raise
