from pydantic import BaseModel
from datetime import datetime
from typing import Any
from typing import Optional


# Pydantic models for user data validation and representation
# These would typically live in a separate 'schemas.py' file.
class GetUser(BaseModel):
    id: Optional[int]
    email: str
    phone_number: Optional[str] = None
    profile_picture: Optional[str] = None
    firstname: str
    lastname: str
    role: str
    subscription_id: Optional[int] = None
    createdOn: Optional[datetime] = None
    updatedOn: Optional[datetime] = None

    class Config:
        from_attributes = True


class CreateUser(BaseModel):
    email: str
    password_hash: str
    firstname: str
    lastname: str
    phone_number: Optional[str] = None
    profile_picture: Optional[str] = None
    role: Optional[str] = "user"
    subscription_id: Optional[int] = None
    createdOn: Optional[datetime] = datetime.now().isoformat()
    updatedOn: Optional[datetime] = None

    class Config:
        from_attributes = True


class GetUserPassword(BaseModel):
    id: int
    email: str
    phone_number: Optional[str] = None
    profile_picture: Optional[str] = None
    firstname: str
    lastname: str
    password_hash: str
    role: str
    subscription_id: Optional[int] = None
    createdOn: Optional[datetime] = None
    updatedOn: Optional[datetime] = None

    class Config:
        from_attributes = True


class RequestUser(BaseModel):
    email: str
    password: str
    firstname: str
    lastname: str
    phone_number: Optional[str] = None
    profile_picture: Optional[str] = None
    role: Optional[str] = "user"
    subscription_id: Optional[int] = None
    createdOn: Optional[datetime] = datetime.now().isoformat()
    updatedOn: Optional[datetime] = None

    class Config:
        from_attributes = True
