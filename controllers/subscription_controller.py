from fastapi import APIRouter, Depends, HTTPException, status
from schemas.subscription_schema import SubscriptionCreate, SubscriptionRead
from services.subscription_services import SubscriptionService
from typing import List

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

def get_subscription_service() -> SubscriptionService:
    return SubscriptionService()

@router.post("/", response_model=SubscriptionRead, status_code=status.HTTP_201_CREATED)
async def create_subscription(
    subscription: SubscriptionCreate,
    service: SubscriptionService = Depends(get_subscription_service),
):
    return await service.create_subscription(subscription)

@router.get("/{subscription_id}", response_model=SubscriptionRead)
async def get_subscription(
    subscription_id: int,
    service: SubscriptionService = Depends(get_subscription_service),
):
    subscription = await service.get_subscription(subscription_id)
    if not subscription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
    return subscription

@router.get("/", response_model=List[SubscriptionRead])
async def get_all_subscriptions(
    service: SubscriptionService = Depends(get_subscription_service),
):
    return await service.get_all_subscriptions()

@router.put("/{subscription_id}", response_model=SubscriptionRead)
async def update_subscription(
    subscription_id: int,
    subscription: SubscriptionCreate,
    service: SubscriptionService = Depends(get_subscription_service),
):
    updated_subscription = await service.update_subscription(subscription_id, subscription)
    if not updated_subscription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
    return updated_subscription

@router.delete("/{subscription_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subscription(
    subscription_id: int,
    service: SubscriptionService = Depends(get_subscription_service),
):
    deleted = await service.delete_subscription(subscription_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
    return None