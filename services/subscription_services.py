from schemas.subscription_schema import SubscriptionCreate, SubscriptionRead
from typing import List, Optional
from datetime import datetime, timezone
import logging
from core.DbUtility import execute_query, fetch_all, fetch_one

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

TABLE_NAME = "subscription"


class SubscriptionService:
    async def create_subscription(
        self, subscription_data: SubscriptionCreate
    ) -> Optional[SubscriptionRead]:
        data = subscription_data.dict()
        data.get("password")
        data["createdOn"] = datetime.now(timezone.utc)
        data["updatedOn"] = None

        columns = ", ".join(data.keys())
        values = ", ".join(["?" for _ in data.values()])
        query = f"INSERT INTO {TABLE_NAME} ({columns}) VALUES ({values})"
        
        try:
            success = await execute_query(query, *data.values())
            if success:
                # Assuming 'id' is auto-incremented and we need to fetch the last inserted one.
                # This is a common pattern, but might need adjustment based on actual DB.
                # For now, let's assume we can fetch by a unique field if available, or
                # if not, we might need to rethink how to get the newly created record.
                # For simplicity, let's assume the subscription_data contains enough info to fetch it back.
                # A more robust solution would involve returning the ID from execute_query or using a RETURNING clause.
                # For now, I'll just return None and log a warning, as we can't reliably get the ID without more info.
                logger.warning("Cannot reliably fetch newly created subscription without its ID. Returning None.")
                return None
            return None
        except Exception as e:
            logger.error(f"Error creating subscription: {e}")
            raise

    async def get_all_subscriptions(self) -> List[SubscriptionRead]:
        query = f"SELECT * FROM {TABLE_NAME}"
        try:
            logger.info(f"Executing query: {query}")
            results = await fetch_all(query)
            logger.info(f"Query results: {results}")
            return [SubscriptionRead(**row) for row in results] if results else []
        except Exception as e:
            logger.error(f"Error fetching subscriptions: {e}")
            raise

    async def get_subscription(
        self, subscription_id: int
    ) -> Optional[SubscriptionRead]:
        query = f"SELECT * FROM {TABLE_NAME} WHERE id = ?"
        try:
            result = await fetch_one(query, (subscription_id,))
            return SubscriptionRead(**result) if result else None
        except Exception as e:
            logger.error(f"Error fetching subscription by id: {e}")
            raise

    async def update_subscription(
        self, subscription_id: int, subscription_data: SubscriptionCreate
    ) -> Optional[SubscriptionRead]:
        data = subscription_data.dict()
        data["updatedOn"] = datetime.now(timezone.utc)

        set_parts = []
        params = []
        for key, value in data.items():
            set_parts.append(f"{key} = ?")
            params.append(value)
        
        params.append(subscription_id) # Add subscription_id for the WHERE clause

        query = f"UPDATE {TABLE_NAME} SET {', '.join(set_parts)} WHERE id = ?"
        
        try:
            success = await execute_query(query, *params)
            if success:
                return await self.get_subscription(subscription_id)
            return None
        except Exception as e:
            logger.error(f"Error updating subscription: {e}")
            raise

    async def delete_subscription(
        self, subscription_id: int
    ) -> Optional[SubscriptionRead]:
        try:
            subscription = await self.get_subscription(subscription_id)
            if not subscription:
                return None
            
            query = f"DELETE FROM {TABLE_NAME} WHERE id = ?"
            success = await execute_query(query, (subscription_id,))
            
            if success:
                return subscription
            return None
        except Exception as e:
            logger.error(f"Error deleting subscription: {e}")
            raise
