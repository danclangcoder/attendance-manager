from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import BaseModel

if TYPE_CHECKING:
    from .student_model import StudentModel
    from .classes_model import ClassesModel


class SectionModel(BaseModel):
    __tablename__ = "section"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    # one-to-many: one section -> many students (FK lives on StudentModel)
    students: Mapped[list["StudentModel"]] = relationship(back_populates="section")
    # one-to-many: one section -> many subject/class entries taught in it
    classes: Mapped[list["ClassesModel"]] = relationship(back_populates="section")
