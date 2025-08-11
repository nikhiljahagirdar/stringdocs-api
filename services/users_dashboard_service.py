from core.DbUtility import fetch_all, fetch_one

class UsersDashboardService:
    async def get_user_count(self) -> dict:
        query = 'SELECT COUNT(*) FROM "user"'
        try:
            count = await fetch_one(query)
            return {"user_count": count[0] if count else 0}
        finally:
            pass

    async def get_document_count(self) -> dict:
        query = "SELECT COUNT(*) FROM pdffile"
        try:
            count = await fetch_one(query)
            return {"document_count": count[0] if count else 0}
        finally:
            pass

    async def get_total_revenue(self) -> dict:
        query = "SELECT SUM(amount) FROM userpayment"
        try:
            revenue = await fetch_one(query)
            return {"total_revenue": revenue[0] if revenue else 0}
        finally:
            pass

    async def get_subscription_count(self) -> dict:
        query = "SELECT COUNT(*) FROM subscription"
        try:
            count = await fetch_one(query)
            return {"subscription_count": count[0] if count else 0}
        finally:
            pass

    async def get_user_documents(self, user_id: int) -> list:
        query = "SELECT * FROM pdffile WHERE user_id = %s"
        try:
            documents = await fetch_all(query, (user_id,))
            return documents
        finally:
            pass

    async def get_user_payments(self, user_id: int) -> list:
        query = '''
            SELECT up.*
            FROM userpayment up
            JOIN usersubscription us ON up.user_subscription_id = us.id
            WHERE us.user_id = %s
        '''
        try:
            payments = await fetch_all(query, (user_id,))
            return payments
        finally:
            pass

    async def get_user_subscriptions(self, user_id: int) -> list:
        query = "SELECT * FROM usersubscription WHERE user_id = %s"
        try:
            subscriptions = await fetch_all(query, (user_id,))
            return subscriptions
        finally:
            pass

    async def get_user_details(self, user_id: int) -> dict:
        query = 'SELECT * FROM "user" WHERE id = %s'
        try:
            user_details = await fetch_one(query, (user_id,))
            return user_details
        finally:
            pass