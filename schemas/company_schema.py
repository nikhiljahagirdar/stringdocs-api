from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, HttpUrl


class CompanyBase(BaseModel):
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    phone_number: Optional[str] = None
    company_email: Optional[str] = None
    company_website: Optional[str] = None
    logo: Optional[str] = None
    subscription_id: Optional[int] = None


class CompanyCreate(CompanyBase):
    pass

    class Config:
        from_attributes = True


class CompanyUpdate(CompanyBase):
    id: Optional[int] = None
    pass

    class Config:
        from_attributes = True


class CompanyRead(CompanyBase):
    id: int
    createdOn: Optional[datetime] = None
    updatedOn: Optional[datetime] = None
    pass

    class Config:
        from_attributes = True


class Company(CompanyBase):
    id: Optional[int] = None

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}
