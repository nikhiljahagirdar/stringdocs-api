from fastapi import APIRouter, Depends, HTTPException
from schemas.user_subscription_schema import UserSubscriptionCreate
from schemas.user_payment_schema import UserPaymentCreate
from services.subscription_services import SubscriptionService
from services.user_payment_service import create_user_payment
import stripe
import os

router = APIRouter(prefix="/payment", tags=["payment"])

stripe.api_key = os.getenv("STRIPE_API_KEY")


async def get_Subscription_service():
    return SubscriptionService()


@router.post("/create-checkout-session")
async def create_checkout_session(
    user_subscription: UserPaymentCreate,
    subscription_service: SubscriptionService = Depends(get_Subscription_service),
):


    session = stripe.Subscription.create(
        billing_mode="subscription",
        customer=user_subscription.customer_email,
        line_items=[
            {
                "price": user_subscription.price_id,
                "quantity": 1,
            }
        ],
    )
    return session.url


@router.post("/stripe-webhook")
async def stripe_webhook(payload: dict):
    event = None
    try:
        event = stripe.Event.construct_from(payload, stripe.api_key)
    except ValueError as e:
        # Invalid payload
        raise HTTPException(status_code=400, detail=str(e))

    # Handle the event
    if event.type == "checkout.session.completed":
        session = event.data.object
        # Create a new user subscription in your database
        # You'll need to extract the relevant information from the session object
        # and create a UserSubscriptionCreate object to pass to your service.
        pass
    elif event.type == "invoice.payment_succeeded":
        invoice = event.data.object
        # Create a new user payment in your database
        # You'll need to extract the relevant information from the invoice object
        # and create a UserPaymentCreate object to pass to your service.
        pass
    else:
        print("Unhandled event type {}".format(event.type))

    return {"status": "success"}
