from fastapi import APIRouter, Depends, HTTPException
from schemas.dashboard_schema import DashboardDataForUser, DashboardDataForAdmin
from services.dashboard_service import DashboardService

# Assuming you have a dependency for getting the current user
from dependencies import get_current_user
from typing import Dict, Any

router = APIRouter()

# Instantiate the service
dashboard_service = DashboardService()


@router.get(
    "/user-dashboard/{user_id}",
    response_model=DashboardDataForUser,  # <--- THIS IS THE KEY FIX
    status_code=200,
)
async def get_user_dashboard(
    user_id: int,
    # user: Dict[str, Any] = Depends(get_current_user) # Assuming user dependency
):
    """
    Endpoint to retrieve dashboard data for a regular user.
    """
    # Assuming user authentication is handled and you have the user_id
    # if user['id'] != user_id and user['role'] != 'admin':
    #     raise HTTPException(status_code=403, detail="Not authorized to view this dashboard.")

    try:
        dashboard_data = await dashboard_service.get_dashboard_data_for_user(user_id)
        # If the service returns a message (e.g., user not found), handle that gracefully
        if dashboard_data.message:
            raise HTTPException(status_code=404, detail=dashboard_data.message)
        return dashboard_data
    except Exception as e:
        # The service will raise an exception on a database error, so we catch it here.
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get(
    "/admin-dashboard",
    response_model=DashboardDataForAdmin,  # <--- THIS IS THE KEY FIX
    status_code=200,
)
async def get_admin_dashboard(
    # user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Endpoint to retrieve global dashboard data for an admin.
    """
    # if user['role'] != 'admin':
    #     raise HTTPException(status_code=403, detail="Not authorized to view the admin dashboard.")

    try:
        return await dashboard_service.get_dashboard_data_for_admin()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
