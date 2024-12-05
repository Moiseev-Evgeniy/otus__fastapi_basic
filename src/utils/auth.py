from datetime import datetime, timezone, timedelta
from uuid import uuid4

import jwt
from passlib.context import CryptContext
from fastapi import Request, HTTPException, status, Depends

from common.settings import settings
from db.connector import AsyncSession
from db.tables import User
from repositories.users import UsersRepository
from utils.enums import TokenType

pwd_context = CryptContext(schemes=["bcrypt"])


def get_hashed_pwd(pwd: str) -> str:
    return pwd_context.hash(pwd)


def verify_pwd(plain_pwd: str, hashed_pwd: str) -> bool:
    return pwd_context.verify(plain_pwd, hashed_pwd)


def create_tokens(data: dict, access_time_delta: int, refresh_time_delta: int):
    to_encode = data.copy()
    datetime_now = datetime.now(timezone.utc)
    expire = datetime_now + timedelta(minutes=access_time_delta)
    to_encode.update({
        "exp": expire,
        "iss": settings.SERVICE_NAME,
        "nbf": datetime_now,
        "iat": datetime_now,
        "jti": str(uuid4()),
    })
    access_token = jwt.encode(
        payload=to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM, headers={"typ": TokenType.access}
    )

    refresh_jti = str(uuid4())
    expire = datetime_now + timedelta(minutes=refresh_time_delta)
    to_encode.update({"exp": expire, "jti": refresh_jti})
    refresh_token = jwt.encode(
        payload=to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM, headers={"typ": TokenType.refresh}
    )

    return access_token, refresh_token, refresh_jti


def get_token(request: Request) -> str:
    if not (token := request.cookies.get("access_token")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found")
    return token


async def get_current_user(token: str = Depends(get_token)) -> User:
    try:
        token_data = jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    if not (user_id := token_data.get("sub")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    async with AsyncSession() as session:
        user = await UsersRepository.get_user(session, user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token data")

    return user
