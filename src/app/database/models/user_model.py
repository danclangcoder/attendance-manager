from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import BaseModel

if TYPE_CHECKING:
    from .app_settings import AppSettings
    from .classes_model import ClassesModel


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(100))
    email: Mapped[str | None] = mapped_column(String(100), default=None)

    # one-to-one: a teacher has at most one active session
    session: Mapped["UserSession | None"] = relationship(back_populates="user")
    # one-to-one: a teacher has at most one linked Google account
    google_account: Mapped["GoogleAccount | None"] = relationship(back_populates="user")
    # one-to-many: a teacher can have many settings rows
    settings: Mapped[list["AppSettings"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    # one-to-many: a teacher can teach many classes
    classes: Mapped[list["ClassesModel"]] = relationship(back_populates="teacher")


class UserSession(BaseModel):
    __tablename__ = "active_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    # unique=True is what actually makes this one-to-one instead of one-to-many
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)

    user: Mapped[UserModel] = relationship(back_populates="session")


class GoogleAccount(BaseModel):
    __tablename__ = "google_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    google_id: Mapped[int] = mapped_column(Integer)
    email: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))

    user: Mapped[UserModel] = relationship(back_populates="google_account")
