from schemas.user_payment_schema import UserPaymentCreate
from core.DbUtility import execute_query

async def create_user_payment(payment: UserPaymentCreate):
    try:
        await execute_query(
            'INSERT INTO "userpayment" (user_subscription_id, stripe_payment_id, amount, currency, status, payment_date) VALUES (%s, %s, %s, %s, %s, %s)',
            (payment.user_subscription_id, payment.stripe_payment_id, payment.amount, payment.currency, payment.status, payment.payment_date)
        )
    except Exception as e:
        raise e