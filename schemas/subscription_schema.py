from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SubscriptionBase(BaseModel):
    id: int
    monthly_price: float
    yearly_price: float
    plan_name: str
    plan_details: str
    stripe_monthly_price_id: str
    stripe_yearly_price_id: str
    plan_details: str


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionRead(SubscriptionBase):
    id: int
    createdon: Optional[datetime]
    updatedon: Optional[datetime]

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}
