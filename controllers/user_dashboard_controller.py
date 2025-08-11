from services.user_dashboard_service import DashboardService
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse


async def get_dashboard_service() -> DashboardService:
    return DashboardService()


router = APIRouter(prefix="/user-dashboard", tags=["User Dashboard"])


@router.get("/user/{user_id}")
async def get_user_dashboard(
    user_id: int, dashboard_service: DashboardService = Depends(get_dashboard_service)
):
    try:
        dashboard_data = await dashboard_service.get_dashboard_data_for_user(user_id)
        return dashboard_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
