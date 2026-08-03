from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import BaseModel

if TYPE_CHECKING:
    from .classes_model import ClassesModel


class SubjectModel(BaseModel):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    code: Mapped[str] = mapped_column(String(16))

    # one-to-many: one subject -> many class entries (one per section it's taught in)
    classes: Mapped[list["ClassesModel"]] = relationship(back_populates="subject")
