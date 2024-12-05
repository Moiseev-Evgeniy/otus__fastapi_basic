"""User schemas."""

from pydantic import BaseModel, Field, EmailStr, field_validator

from utils.enums import UserRole


class UserBase(BaseModel):
    name: str = Field(min_length=5, max_length=30, example="Vasya")
    login: str = Field(min_length=5, max_length=30, example="Terminator_666")
    email: EmailStr = Field(min_length=5, max_length=30, example="vasya_killer@mail.net")
    role: UserRole = Field(default=UserRole.user, example=UserRole.user)

    @field_validator("email")
    @classmethod
    def email_normalize(cls, value: str) -> str:
        return value.lower()


class UserCreate(UserBase):
    pwd: str = Field(min_length=5, max_length=30, serialization_alias="hashed_pwd")


class RefreshToken(BaseModel):
    refresh_token: str


class UserAuth(BaseModel):
    login_or_email: str = Field(min_length=5, max_length=30, example="vasya_killer@mail.net")
    pwd: str = Field(min_length=5, max_length=30)
