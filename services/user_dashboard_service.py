from core.db.asynccrud import (
    custom_query_one,
    custom_query_all,
)
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime

# Import the new Pydantic schemas
from schemas.dashboard_schema import (
    DashboardDataForUser,
    UserFileMetrics,
    RecentFile,
    CompanyFileMetrics,
    CompanyDashboard,
    UserDashboard,
    DashboardDataForAdmin,
    AdminSummary,
    AdminRecentFile,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class DashboardService:
    async def get_dashboard_data_for_user(self, user_id: int) -> DashboardDataForUser:
        try:
            user_query = """
                SELECT
                    u.id,
                    u.role,
                    c.id AS company_id,
                    c.name AS company_name
                FROM users u
                LEFT JOIN usercompany uc ON u.id = uc.user_id
                LEFT JOIN company c ON uc.company_id = c.id
                WHERE u.id = %s;
            """
            user_data = await custom_query_one(user_query, (user_id,))
            logger.info(f"User data: {user_data}")

            if not user_data:
                return DashboardDataForUser(
                    user_dashboard=UserDashboard(
                        user_file_metrics=UserFileMetrics(
                            total_my_files=0,
                            my_completed_files=0,
                            my_failed_files=0,
                            my_pending_files=0,
                        ),
                        recent_files=[],
                    ),
                    message="User not found.",
                )

            company_dashboard = None
            if user_data["company_id"]:
                company_id = user_data["company_id"]

                company_files_query = """
                    SELECT
                        COUNT(pf.id) AS total_company_files,
                        SUM(CASE WHEN pf.status = 'completed' THEN 1 ELSE 0 END) AS completed_files,
                        SUM(CASE WHEN pf.status = 'pending' THEN 1 ELSE 0 END) AS pending_files
                    FROM pdffile pf
                    JOIN users u ON pf.user_id = u.id
                    JOIN usercompany uc ON u.id = uc.user_id
                    WHERE uc.company_id = %s;
                """
                company_file_metrics_data = await custom_query_one(
                    company_files_query, (company_id,)
                )
                company_file_metrics = CompanyFileMetrics(**company_file_metrics_data)
                logger.info(f"Company file metrics: {company_file_metrics}")


                company_file_status_query = """
                    SELECT
                        pf.status,
                        COUNT(pf.id) AS count
                    FROM pdffile pf
                    JOIN users u ON pf.user_id = u.id
                    JOIN usercompany uc ON u.id = uc.user_id
                    WHERE uc.company_id = %s
                    GROUP BY pf.status;
                """
                company_file_status_results = await custom_query_all(
                    company_file_status_query, (company_id,)
                )
                logger.info(f"Company file status results: {company_file_status_results}")
                company_file_status_map = {
                    row["status"]: row["count"] for row in company_file_status_results
                }

                company_dashboard = CompanyDashboard(
                    company_name=user_data["company_name"],
                    file_metrics=company_file_metrics,
                    file_status_breakdown=company_file_status_map,
                )

            user_files_query = """
                SELECT
                    COUNT(id) AS total_my_files,
                    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS my_completed_files,
                    SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) AS my_failed_files,
                    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) AS my_pending_files
                FROM pdffile
                WHERE user_id = %s;
            """
            user_file_metrics_data = await custom_query_one(
                user_files_query, (user_id,)
            )
            logger.info(f"User file metrics data: {user_file_metrics_data}")
            user_file_metrics = UserFileMetrics(**user_file_metrics_data)

            recent_files_query = """
                SELECT
                    id,
                    filename,
                    status,
                    createdon
                FROM pdffile
                WHERE user_id = %s
                ORDER BY createdon DESC
                LIMIT 5;
            """
            recent_files_data = await custom_query_all(recent_files_query, (user_id,))
            recent_files = [RecentFile(**row) for row in recent_files_data]
            

            user_dashboard = UserDashboard(
                user_file_metrics=user_file_metrics, recent_files=recent_files
            )

            return DashboardDataForUser(
                user_dashboard=user_dashboard, company_dashboard=company_dashboard
            )
        except Exception as e:
            logger.error(
                f"Error fetching user dashboard data for user_id {user_id}: {e}"
            )
            raise

    async def get_dashboard_data_for_admin(self) -> DashboardDataForAdmin:
        try:
            summary_query = """
                SELECT
                    (SELECT COUNT(*) FROM users) AS total_users,
                    (SELECT COUNT(*) FROM company) AS total_companies,
                    (SELECT COUNT(*) FROM pdffile) AS total_files,
                    (SELECT COUNT(*) FROM usersubscription WHERE status = 'active') AS total_active_subscriptions;
            """
            summary_data = await custom_query_one(summary_query, ())
            summary = AdminSummary(**summary_data)

            file_status_query = """
                SELECT
                    status,
                    COUNT(*) AS count
                FROM pdffile
                GROUP BY status;
            """
            file_status_results = await custom_query_all(file_status_query, ())
            file_status_map = {
                row["status"]: row["count"] for row in file_status_results
            }

            recent_files_query = """
                SELECT
                    p.filename,
                    p.status,
                    p.createdOn,
                    u.email AS user_email
                FROM pdffile p
                JOIN users u ON p.user_id = u.id
                ORDER BY p.createdOn DESC
                LIMIT 10;
            """
            recent_files_data = await custom_query_all(recent_files_query, ())
            recent_files = [AdminRecentFile(**row) for row in recent_files_data]

            subscription_status_query = """
                SELECT
                    status,
                    COUNT(*) AS count
                FROM usersubscription
                GROUP BY status;
            """
            subscription_status_results = await custom_query_all(
                subscription_status_query, ()
            )
            subscription_status_map = {
                row["status"]: row["count"] for row in subscription_status_results
            }

            return DashboardDataForAdmin(
                summary=summary,
                file_status_breakdown=file_status_map,
                recent_files=recent_files,
                subscription_status_breakdown=subscription_status_map,
            )
        except Exception as e:
            logger.error(f"Error fetching admin dashboard data: {e}")
            raise
