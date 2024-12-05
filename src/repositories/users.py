from uuid import uuid4

from sqlalchemy import select, delete, and_

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
        query = select(User.id, User.hashed_pwd, User.role).where(getattr(User, column_name) == value)
        result = await session.execute(query)
        return result.one_or_none()

    @staticmethod
    async def get_user(session: AsyncSession, user_id: str) -> User | None:
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        return result.scalar()

    @staticmethod
    async def delete_refresh_token(session: AsyncSession, user_id: str, user_agent: str):
        query = delete(Token).where(and_(Token.subject == user_id, Token.user_agent == user_agent))
        await session.execute(query)
