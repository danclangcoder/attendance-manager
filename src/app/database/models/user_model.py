from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(100))
    email: Mapped[str | None] = mapped_column(String(100), default=None)

    session: Mapped[UserSession | None] = relationship(back_populates="user")

class UserSession(BaseModel):
    __tablename__ = "active_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped[UserModel] = relationship(back_populates="session")