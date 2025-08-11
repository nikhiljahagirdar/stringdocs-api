from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class UserFileMetrics(BaseModel):
    total_my_files: int
    my_completed_files: Optional[int]
    my_failed_files: Optional[int]
    my_pending_files: Optional[int]

    class config:
        from_attributes = True


class RecentFile(BaseModel):
    id: int
    filename: str
    status: str
    createdon: datetime

    class config:
        from_attributes = True


class CompanyFileMetrics(BaseModel):
    total_company_files: Optional[int]
    completed_files: Optional[int]
    pending_files: Optional[int]

    class config:
        from_attributes = True


class CompanyDashboard(BaseModel):
    company_name: str
    file_metrics: CompanyFileMetrics
    file_status_breakdown: Dict[str, int]

    class config:
        from_attributes = True


class UserDashboard(BaseModel):
    user_file_metrics: UserFileMetrics
    recent_files: List[RecentFile]

    class config:
        from_attributes = True


class DashboardDataForUser(BaseModel):
    user_dashboard: UserDashboard
    company_dashboard: Optional[CompanyDashboard] = None
    message: Optional[str] = None

    class config:
        from_attributes = True


# --- Admin Schemas ---


class AdminSummary(BaseModel):
    total_users: int
    total_companies: int
    total_files: int
    total_active_subscriptions: int

    class config:
        from_attributes = True


class AdminFileStatusBreakdown(BaseModel):
    status: str
    count: int

    class config:
        from_attributes = True


class AdminRecentFile(BaseModel):
    filename: str
    status: str
    createdon: datetime
    user_email: str

    class config:
        from_attributes = True


class DashboardDataForAdmin(BaseModel):
    summary: AdminSummary
    file_status_breakdown: Dict[
        str, int
    ]  # Or List[AdminFileStatusBreakdown] if you prefer
    recent_files: List[AdminRecentFile]
    subscription_status_breakdown: Dict[str, int]

    class config:
        from_attributes = True
