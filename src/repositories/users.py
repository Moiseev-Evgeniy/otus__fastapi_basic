from uuid import uuid4

from db.connector import AsyncSession
from db.tables import User, Token


class UsersRepository:

    @staticmethod
    async def insert_user_data(session: AsyncSession, user_data: dict) -> uuid4:
        user_id = uuid4()
        user = User(id=user_id, **user_data)
        session.add(user)
        return user_id

    @staticmethod
    async def insert_refresh_token_data(session: AsyncSession, token_data: dict):
        token = Token(**token_data)
        session.add(token)
