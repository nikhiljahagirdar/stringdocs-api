from datetime import timedelta
import os
import logging
from fastapi import HTTPException, status
from core.security import hash_password, verify_password, create_access_token
from services.user_service import UserService
from services.company_service import CompanyService
from services.user_comapny_service import UserCompanyService
from schemas.user_schema import CreateUser
from schemas.auth_schema import GetUserLogin
from schemas.company_schema import CompanyCreate
from schemas.user_company_schema import UserCompanyCreate
from schemas.auth_schema import Register, Login

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class AuthService:
    def __init__(self):
        self.user_service = UserService()
        self.company_service = CompanyService()
        self.user_company_service = UserCompanyService()

    async def register_user(self, user_data: Register):
        logger.info(f"Registering user with data: {user_data}")
        hashed_password = hash_password(user_data.password)
        existing_user = await self.user_service.get_user_by_email(user_data.email)
        logger.info(f"Existing user: {existing_user}")
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        if user_data.account_type == "company":
            company_data = CompanyCreate(
                name=user_data.company_name,
                address=user_data.address,
                city=user_data.city,
                state=user_data.state,
                zip_code=user_data.zip_code,
                country=user_data.country,
                phone_number=user_data.company_phone_number,
                company_email=user_data.company_email,
                subscription_id=user_data.subscription_id,
                logo=user_data.company_logo,
            )
            created_company = await self.company_service.create_company(company_data)
            logger.info(
                "========================================================================================================"
            )
            logger.info(f"company data: {company_data}")
            logger.info(
                "========================================================================================================"
            )
            add_user = CreateUser(
                firstname=user_data.firstname,
                lastname=user_data.lastname,
                email=user_data.email,
                password_hash=hashed_password,
                phone_number=user_data.phone_number,
                role="user",
            )
            created_user = await self.user_service.create_user(add_user)
            logger.info(
                "========================================================================================================"
            )
            logger.info(f"user data: {created_user}")
            logger.info(
                "========================================================================================================"
            )
            create_user_company = UserCompanyCreate(
                user_id=created_user.id, company_id=created_company.id
            )
            created_user_company = await self.user_company_service.create_user_company(
                create_user_company
            )
            logger.info(f"created user company: {created_user_company}")
            return "USER CREATED"

    async def login_user(self, login_data: Login):
        """
        Authenticates a user and returns an access token upon successful login.
        """
        user = await self.user_service.get_user_by_email(login_data.email)
        logger.info(f"user: {user}")
        if not user or not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(subject=user.email)
        return {
            "id": user.id,
            "email": user.email,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "company_id": 0,
            "role": user.role,
            "access_token": access_token,
            "token_type": "bearer",
            "subscription_id": user.subscription_id,
        }
