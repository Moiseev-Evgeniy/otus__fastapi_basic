"""User schemas."""

from fastapi import Query
from pydantic import BaseModel, Field, EmailStr

from utils.enums import UserRole


class UserBase(BaseModel):
    name: str = Field(max_length=30, example="Vasya")
    login: str = Field(max_length=30, example="Terminator_666")
    email: EmailStr = Field(max_length=30, example="vasya_killer@mail.net")
    role: UserRole = Field(default=UserRole.user, example=UserRole.user)


class UserCreate(UserBase):
    pwd: str = Field(serialization_alias="hashed_pwd")


class Tokens(BaseModel):
    access_token: str
    refresh_token: str
