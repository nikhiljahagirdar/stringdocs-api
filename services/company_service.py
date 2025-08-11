from core.db.asynccrud import (
    select_all,
    select_where,
    insert,
    update,
    delete,
    select_where_single,
)
from schemas.company_schema import CompanyCreate, CompanyRead
from typing import Optional, List
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class CompanyService:
    async def create_company(self, company: CompanyCreate) -> Optional[CompanyRead]:
        """
        Creates a new company entry in the database.
        """
        try:
            insert_data = company.dict()
            result = await insert("company", insert_data)
            if result:
                return CompanyRead(**result)
            return None
        except Exception as e:
            logging.info(f"Error creating company: {e}")
            raise

    async def get_company(self, company_id: int) -> Optional[CompanyRead]:
        """
        Retrieves a company entry by its ID.
        """
        params = {"id": company_id}
        try:
            result = await select_where_single("company", "id = %s", (company_id,))
            if result:
                return [CompanyRead(**result)] 
            return None
        except Exception as e:
            logging.info(f"Error retrieving company: {e}")
            raise

    async def update_company(
        self, company_id: int, company: CompanyCreate
    ) -> Optional[CompanyRead]:
        """
        Updates an existing company entry in the database.
        """
        try:
            result = await update("company", company_id, company.dict())
            if result:
                all_users = [CompanyRead(**result)]
                return all_users[0]
            return None
        except Exception as e:
            logging.error(f"Error updating company: {e}")
            raise

    async def delete_company(self, company_id: int) -> bool:
        """
        Deletes a company entry from the database.
        """
        try:
            result = await delete("company", company_id)
            return result
        except Exception as e:
            logging.error(f"Error deleting company: {e}")
            raise

    async def list_companies(self) -> List[CompanyRead]:
        """
        Retrieves all company entries from the database.
        """
        try:
            results = await select_all("company")
            return [CompanyRead(**row) for row in results]
        except Exception as e:
            logging.error(f"Error listing companies: {e}")
            raise
