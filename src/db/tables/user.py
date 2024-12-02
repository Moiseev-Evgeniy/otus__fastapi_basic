"""User tables."""

from sqlalchemy import Column, String, UUID, ForeignKey, Enum, Text

from common.settings import settings
from db.tables.base import BaseModel, CreatedAtMixin, IdMixin, UpdatedAtMixin
from utils.enums import UserRole


class User(BaseModel, IdMixin, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "users"

    name = Column(String(30), nullable=False)
    login = Column(String(30), unique=True, nullable=False)
    email = Column(String(30),  unique=True, nullable=False)
    hashed_pwd = Column(Text, nullable=False)
    role = Column(Enum(UserRole), nullable=False)


class Token(BaseModel, CreatedAtMixin):
    __tablename__ = "tokens"

    jti = Column(UUID, primary_key=True, comment="JWT identifier")
    subject = Column(UUID, ForeignKey(f"{settings.DB_SCHEMA}.users.id", ondelete="CASCADE"), nullable=False)
    user_agent = Column(String(100), nullable=False, comment="User device description")
