from pydantic import BaseModel
from datetime import datetime


class UserSubscriptionBase(BaseModel):
    user_id: int
    subscription_id: int
    stripe_customer_id: str
    stripe_subscription_id: str
    status: str
    start_date: datetime
    end_date: datetime | None = None


class UserSubscriptionCreate(BaseModel):
    user_id: int
    subscription_id: int
    stripe_customer_id: str
    stripe_subscription_id: str
    status: str
    start_date: datetime
    end_date: datetime | None = None

    class Config:
        from_attributes = True


class UserSubscription(UserSubscriptionBase):
    id: int
    user_id: int
    subscription_id: int
    stripe_customer_id: str
    stripe_subscription_id: str
    status: str
    start_date: datetime
    end_date: datetime | None = None
    createdOn: datetime
    updatedOn: datetime | None = None

    class Config:
        from_attributes = True
