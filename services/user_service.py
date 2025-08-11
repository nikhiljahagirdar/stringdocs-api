from core.security import hash_password
from core.db.asynccrud import (
    select_all,
    select_where,
    insert,
    update,
    delete,
    select_where_single,
    custom_query_one,
)
import logging
from typing import List, Optional, Dict, Any
from schemas.user_schema import GetUser, CreateUser, GetUserPassword
from datetime import datetime
from core.DbUtility import fetch_one, execute_query, fetch_all

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserService:
    """
    A service class for managing CRUD operations for users in the database.
    """

    async def create_user(self, user_data: CreateUser):
        """
        Creates a new user in the database.
        The 'id' is generated automatically by the database.
        """
        insert_data = user_data.dict()
        data = await insert("users", insert_data)
        return GetUserPassword(**data)

    async def get_user_by_id(self, user_id: int) -> Optional[GetUserPassword]:
        """
        Retrieves a user by their ID from the database.
        """

        user = await select_where_single("users", "id = %s", (user_id,))
        if user:
            return GetUserPassword(**user)
        return None

    async def get_user_by_email(self, email: str) -> Optional[GetUserPassword]:
        """
        Retrieves a user by their email from the database.
        """
        user = await select_where_single("users", "email = %s", (email,))
        if user:
            return GetUserPassword(**user)
        return None

    async def get_all_users(self) -> List[GetUser]:
        """
        Retrieve all users from the database.
        """
        users = await select_all("users")
        if users:
            return [GetUser(**user) for user in users]
        return []

    async def update_user(self, user_id: int, update_data: Dict[str, Any]) -> bool:
        """
        Updates an existing user's data in the database.
        """
        if "password" in update_data:
            update_data["password_hash"] = hash_password(update_data.pop("password"))

        update_data["updatedOn"] = datetime.utcnow()
        try:
            await update("users", update_data, "id = %s", (user_id,))
            return True
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            return False

    async def delete_user(self, user_id: int) -> bool:
        """
        Deletes a user from the database.
        """
        try:
            await delete("users", "id = %s", (user_id,))
            return True
        except Exception as e:
            logger.error(f"Error deleting user: {e}")
            return False
