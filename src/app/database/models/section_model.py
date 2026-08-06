from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import BaseModel

if TYPE_CHECKING:
    from .classes_model import ClassesModel
    from .course_model import CourseModel
    from .student_model import StudentModel


class SectionModel(BaseModel):
    __tablename__ = "section"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"))
    year_level: Mapped[str] = mapped_column(String(16))

    students: Mapped[list["StudentModel"]] = relationship(back_populates="section")
    classes: Mapped[list["ClassesModel"]] = relationship(back_populates="section")
    course: Mapped["CourseModel"] = relationship(back_populates="sections")
