from __future__ import annotations

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import BaseModel
from .user_model import UserModel


class AppSettings(BaseModel):
    __tablename__ = "app_settings"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    key: Mapped[str] = mapped_column(String(50))
    value: Mapped[str] = mapped_column(String(255))

    user: Mapped[UserModel] = relationship(back_populates="settings")

    __table_args__ = (UniqueConstraint("user_id", "key"),)
