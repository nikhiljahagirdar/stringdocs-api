from core.db.asynccrud import (
    select_all,
    select_where,
    insert,
    update,
    delete,
    select_where_single,
)
from schemas.user_company_schema import UserCompanyCreate, UserCompanyRead
from schemas.company_schema import CompanyRead  # Assuming CompanyRead schema exists
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class UserCompanyService:
    async def create_user_company(
        self, user_company: UserCompanyCreate
    ) -> Optional[UserCompanyRead]:
        """
        Associates a user with a company in the database.
        """
        insert_data = user_company.dict()
        try:
            result = await insert("usercompany", insert_data)
            if result:
                return UserCompanyRead(**result)
        except Exception as e:
            logging.error(f"Error creating user-company association: {e}")
            raise

    async def get_user_company(self, user_company_id: int) -> Optional[UserCompanyRead]:
        """
        Retrieves a user-company association by its ID.
        """
        user = await select_where_single("usercompany", "id = %s", (user_company_id,))
        if user:
            return UserCompanyRead(**user)
        return None

    async def update_user_company(
        self, user_company_id: int, user_company: UserCompanyCreate
    ) -> Optional[UserCompanyRead]:
        """
        Updates an existing user-company association in the database.
        """
        try:
            result = await update("usercompany", user_company_id, user_company.dict())
            if result:
                return UserCompanyRead(**result)
            return None
        except Exception as e:
            logging.error(f"Error updating user-company association: {e}")
            raise

    async def delete_user_company(self, user_company_id: int) -> bool:
        """
        Deletes a user-company association from the database.
        """

        try:
            deleted_rows = delete("usercompany", user_company_id)
            logger.info(f"Deleted rows: {deleted_rows}")
            return deleted_rows
        except Exception as e:
            logging.error(f"Error deleting user-company association: {e}")
            raise

    async def list_user_companies(self) -> List[UserCompanyRead]:
        """
        Retrieves all user-company associations from the database.
        """
        try:
            query = await select_all("usercompany")
            return [
                UserCompanyRead(
                    id=uc["id"], user_id=uc["user_id"], company_id=uc["company_id"]
                )
                for uc in query
            ]
        except Exception as e:
            logging.error(f"Error listing user-company associations: {e}")
            raise
