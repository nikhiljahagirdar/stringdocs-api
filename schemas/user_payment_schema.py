from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserPaymentBase(BaseModel):
    user_subscription_id: int
    stripe_payment_id: str
    amount: float
    currency: str
    status: str
    payment_date: Optional[datetime] = datetime.now().isoformat()
    createdon: datetime
    updatedon: datetime | None = None

    class config:
        from_attributes = True


class UserPaymentCreate(BaseModel):
    user_subscription_id: int
    stripe_payment_id: str
    amount: float
    currency: str
    customer_email: str

    class config:
        from_attributes = True


class UserPayment(BaseModel):
    id: int
    user_subscription_id: int
    stripe_payment_id: str
    amount: float
    currency: str
    status: str
    payment_date: Optional[datetime] = datetime.now().isoformat()
    createdon: datetime
    updatedon: datetime | None = None

    class Config:
        from_attributes = True
