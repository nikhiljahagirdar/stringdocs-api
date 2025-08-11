from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from schemas.user_schema import CreateUser, GetUser, GetUserPassword, RequestUser
from services.user_service import UserService
from core.security import hash_password
import datetime
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/users", tags=["Users"])

USER_NOT_FOUND = "User not found"


def get_user_service():
    return UserService()


@router.get("/")
async def get_all_users(user_service: UserService = Depends(get_user_service)):
    users = await user_service.get_all_users()
    return [GetUser(**user.model_dump()) for user in users]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: RequestUser, user_service: UserService = Depends(get_user_service)
):
    hashed_password = hash_password(user_data.password)
    data = user_data.dict()

    create_user_data = CreateUser(
        email=data["email"],
        password_hash=hashed_password,
        firstname=data["firstname"],
        lastname=data["lastname"],
        phone_number=data["phone_number"],
        profile_picture=data["profile_picture"],
        role=data["role"],
        subscription_id=data["subscription_id"],
        createdOn=datetime.datetime.now().isoformat(),
    )
    created_record = await user_service.create_user(user_data=create_user_data)
    if not created_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User could not be created."
        )
    return created_record


@router.get("/{user_id}", response_model=GetUserPassword)
async def get_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND
        )
    return user


@router.put("/{user_id}")
async def update_user(
    user_id: int,
    user_data: CreateUser,
    user_service: UserService = Depends(get_user_service),
):
    update_data_dict = user_data.model_dump(exclude_unset=True)
    success = await user_service.update_user(
        user_id=user_id, update_data=update_data_dict
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND
        )
    return {"message": "User updated successfully"}


@router.delete("/{user_id}")
async def delete_user(
    user_id: int, user_service: UserService = Depends(get_user_service)
):
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND
        )
    await user_service.delete_user(user_id)
    return JSONResponse(content={"message": "User deleted successfully"})
