from typing import List, Optional
from schemas.user_schema import GetUser
from core.DbUtility import fetch_all, fetch_one


class AdminService:
    async def get_all_users(self) -> List[GetUser]:
        query = '''
            SELECT id, email, phone_number, profile_picture, firstname, lastname, role, subscription_id,  createdon, updatedon
            FROM "user"
            ORDER BY createdon
        '''
        result = await fetch_all(query)
        if not result:
            return []
        users: List[GetUser] = []
        for user in result:
            users.append(
                GetUser(
                    id=int(user["id"]),
                    email=user["email"],
                    phone_number=user.get("phone_number"),
                    profile_picture=user.get("profile_picture"),
                    firstname=user["firstname"],
                    lastname=user["lastname"],
                    subscription_id=user.get("subscription_id"),
                    role=user["role"],
                    createdOn=user["createdon"],
                    updatedOn=user["updatedon"],
                )
            )
        return users

    async def get_user(self, user_id: int) -> Optional[GetUser]:
        query = '''
            SELECT id, email, phone_number, profile_picture, firstname, lastname, subscription_id, company_id, role, createdon, updatedon
            FROM "user"
            WHERE id = %s
        '''
        row = await fetch_one(query, (user_id,))
        if row:
            return GetUser(
                id=int(row["id"]),
                email=row["email"],
                phone_number=row.get("phone_number"),
                profile_picture=row.get("profile_picture"),
                firstname=row["firstname"],
                lastname=row["lastname"],
                subscription_id=row.get("subscription_id"),
                company_id=row.get("company_id"),
                role=row["role"],
                createdOn=row["createdon"],
                updatedOn=row["updatedon"],
            )
        return None