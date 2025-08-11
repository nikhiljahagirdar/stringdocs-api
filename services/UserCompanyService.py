from core.db.asynccrud import (
    select_all,
    select_where,
    insert,
    update,
    delete,
    select_where_single,
    custom_query_one,
)
from schemas.user_company_schema import UserCompanyCreate, UserCompanyRead
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class UserCompanyService:
    async def create_user_company(
        self,
        user_company: UserCompanyCreate,
    ) -> Optional[UserCompanyRead]:
        """
        Creates a new user-company relationship entry in the database.
        """
        try:
            result = await insert('usercompany',user_company.dict())
            if result:
                return UserCompanyRead(**result)
            return None
        except Exception as e:
            logging.error(f"Error creating user-company link: {e}")
            raise
        
        
 


    async def get_user_company(self, user_company_id: int) -> Optional[UserCompanyRead]:
        """
        Retrieves a user-company relationship by its ID.
        """
        try:
            result = await select_where_single("usercompany", "id = %s",(user_company_id,))
            if result:
                return UserCompanyRead(**result)
            return None
        except Exception as e:
            logging.error(f"Error getting user-company link: {e}")
            raise

    async def get_all_user_companies(self) -> List[UserCompanyRead]:
        """
        Retrieves all user-company relationship entries.
        """
        try:
            results = await select_where("usercompany"))
            return [UserCompanyRead(**row) for row in results]
        except Exception as e:
            logging.error(f"Error getting all user-company links: {e}")
            raise

    async def update_user_company(
        self, user_company_id: int, user_company: UserCompanyCreate
    ) -> Optional[UserCompanyRead]:
        """
        Updates a user-company relationship.
        """
        try:
            result = await update("usercompany", user_company.dict(), "id = %s", (user_company_id,))
            if result:
                return UserCompanyRead(**result)
            return None
        except Exception as e:
            logging.error(f"Error updating user-company link: {e}")
            raise

    async def delete_user_company(self, user_company_id: int) -> bool:
        """
        Deletes a user-company relationship by ID.
        """
        try:
            result = await delete("usercompany", "id = %s", (user_company_id,))
            return result is not None
        except Exception as e:
            logging.error(f"Error deleting user-company link: {e}")
            raise
        
    
    