from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .session import CurrentSession


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    username: Mapped[str] = mapped_column(String(64), unique=True)
    email: Mapped[str | None] = mapped_column(String(255), unique=True, default=None)
    password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(32))

    current_session: Mapped['CurrentSession | None'] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
    )
