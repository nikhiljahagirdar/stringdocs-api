from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from schemas.auth_schema import GoogleAuth, Login, Register
from services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_auth_service() -> AuthService:
    return AuthService()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: Register,
    auth_service: AuthService = Depends(get_auth_service),
):
    user = await auth_service.register_user(user_data)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "User registered successfully"},
    )


@router.post("/login")
async def login_for_access_token(
    login_data: Login,
    auth_service: AuthService = Depends(get_auth_service),
):
    token_data = await auth_service.login_user(login_data)
    return JSONResponse(status_code=status.HTTP_200_OK, content=token_data)


@router.post("/google-auth")
async def google_auth(
    google_auth_data: GoogleAuth,
    auth_service: AuthService = Depends(get_auth_service),
):
    token_data = await auth_service.google_auth(google_auth_data)
    return JSONResponse(status_code=status.HTTP_200_OK, content=token_data)
