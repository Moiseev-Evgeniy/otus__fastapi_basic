from datetime import datetime, timezone, timedelta
from uuid import uuid4

import jwt
from passlib.context import CryptContext

from common.settings import settings
from utils.enums import TokenType

pwd_context = CryptContext(schemes=["bcrypt"])


def get_hashed_pwd(pwd: str) -> str:
    return pwd_context.hash(pwd)


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
