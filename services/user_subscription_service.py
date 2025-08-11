from schemas.user_subscription_schema import UserSubscriptionCreate
from core.DbUtility import execute_query

async def create_user_subscription(subscription: UserSubscriptionCreate):
    try:
        await execute_query(
            'INSERT INTO "usersubscription" (user_id, subscription_id, stripe_customer_id, stripe_subscription_id, status, start_date, end_date) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (subscription.user_id, subscription.subscription_id, subscription.stripe_customer_id, subscription.stripe_subscription_id, subscription.status, subscription.start_date, subscription.end_date)
        )
    except Exception as e:
        raise e