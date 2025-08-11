from core.db.asynccrud import (
    select_all,
    select_where,
    select_where_single,
    insert,
    update,
    delete,
    custom_query_one,
)
from schemas.status_schema import SiteStatusCreate, SiteStatusRead
from typing import Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class StatusService:
    async def create_site_status(
        self,
        site_status: SiteStatusCreate,
    ) -> Optional[SiteStatusRead]:
        """
        Creates a new site status entry in the database.

        Args:
            site_status: The SiteStatusCreate object containing the data for the new entry.

        Returns:
            The created site status entry as a SiteStatusRead object.
        """
        try:
            result = await insert("sitestatus", site_status.model_dump())
            if result:
                return SiteStatusRead(**result)
            return None
        except Exception as e:
            logging.error(f"Error creating site status: {e}")
            raise

    async def get_site_status(self, site_status_id: int) -> Optional[SiteStatusRead]:
        """
        Retrieves a site status entry by its ID.

        Args:
            site_status_id: The ID of the site status entry to retrieve.

        Returns:
            The site status entry as a SiteStatusRead object if found, otherwise None.
        """
        try:
            result = await select_where_single(
                "sitestatus", "id = %s", (site_status_id,)
            )
            if result:
                return SiteStatusRead(**result)
            return None
        except Exception as e:
            logging.error(f"Error getting site status: {e}")
            raise

    async def get_all_site_statuses(self) -> List[SiteStatusRead]:
        """
        Retrieves all site status entries.
        Returns:
            A list of site status entries as SiteStatusRead objects.
        """
        try:
            results = await select_all("sitestatus")
            return [SiteStatusRead(**row) for row in results]
        except Exception as e:
            logging.error(f"Error getting all site statuses: {e}")
            raise

    async def update_site_status(
        self, site_status_id: int, site_status: SiteStatusCreate
    ) -> Optional[SiteStatusRead]:
        """
        Updates an existing site status entry.

        Args:
            site_status_id: The ID of the site status entry to update.
            site_status: The SiteStatusCreate object containing the updated data.

        Returns:
            The updated site status entry as a SiteStatusRead object if updated, otherwise None.
        """
        try:
            result = await update(
                "sitestatus", site_status.model_dump(), "id = %s", (site_status_id,)
            )
            if result:
                return SiteStatusRead(**result)
            return None
        except Exception as e:
            logging.error(f"Error updating site status: {e}")
            raise

    async def delete_site_status(self, site_status_id: int) -> bool:
        """
        Deletes a site status entry by its ID.

        Args:
            site_status_id: The ID of the site status entry to delete.

        Returns:
            True if the entry was deleted, False otherwise.
        """
        try:
            result = await delete("sitestatus", "id = %s", (site_status_id,))
            return result is not None
        except Exception as e:
            logging.error(f"Error deleting site status: {e}")
            raise
