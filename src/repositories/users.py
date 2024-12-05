from uuid import uuid4

from sqlalchemy import select

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
    async def insert_refresh_token_data(session: AsyncSession, token_data: dict) -> None:
        token = Token(**token_data)
        session.add(token)

    @staticmethod
    async def get_user_data(session: AsyncSession, value: str, column_name: str) -> User | None:
        query = select(User.id, User.hashed_pwd).where(getattr(User, column_name) == value)
        result = await session.execute(query)
        return result.one_or_none()

    @staticmethod
    async def get_user(session: AsyncSession, user_id: str) -> User | None:
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        return result.scalar()
