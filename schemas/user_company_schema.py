from pydantic import BaseModel


class UserCompanyCreate(BaseModel):
    user_id: int
    company_id: int

    class Config:
        from_attributes = True


class UserCompanyRead(BaseModel):
    id: int
    user_id: int
    company_id: int

    class Config:
        from_attributes = True
