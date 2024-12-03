"""User service."""
from uuid import uuid4

from fastapi import status, HTTPException
from sqlalchemy.exc import IntegrityError
from user_agents import parse

from common.settings import settings
from db.connector import AsyncSession
from dto.schemas.users import UserCreate, Tokens
from repositories.users import UsersRepository
from utils.auth import get_hashed_pwd, create_tokens
from utils.enums import UserRole


class UserService:

    @classmethod
    async def register_user(cls, user: UserCreate, user_agent: str) -> dict[str, str]:

        user_id = await cls.add_user(user)
        access_token, refresh_token = await cls.get_tokens(user_id, user.role, user_agent)

        return dict(access_token=access_token, refresh_token=refresh_token)

    @staticmethod
    async def add_user(user: UserCreate) -> uuid4:
        user.pwd = get_hashed_pwd(user.pwd)

        async with AsyncSession() as session:
            user_id = await UsersRepository.insert_user_data(session, user.model_dump(by_alias=True))
            try:
                await session.commit()
            except IntegrityError as e:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{e.args[0].split('DETAIL:')[1]}")

        return user_id

    @staticmethod
    async def get_tokens(user_id: uuid4, user_role: UserRole, user_agent: str) -> tuple[str, str]:
        user_agent = str(parse(user_agent))

        token_data = {"sub": {"user_id": str(user_id), "user_agent": user_agent, "role": user_role}}
        access_token, refresh_token, refresh_jti = create_tokens(
            token_data, settings.ACCESS_TOKEN_EXPIRE_MINUTES, settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )

        async with AsyncSession() as session:
            await UsersRepository.insert_refresh_token_data(
                session, {"jti": refresh_jti, "subject": user_id, "user_agent": user_agent}
            )
            try:
                await session.commit()
            except IntegrityError as e:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{e.args[0].split('DETAIL:')[1]}")

        return access_token, refresh_token
