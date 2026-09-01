from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import BaseModel

if TYPE_CHECKING:
    from .classes_model import ClassesModel
    from .student_model import StudentModel


class EnrollmentModel(BaseModel):
    """
    Links a student to a specific class.

    A student can be enrolled in multiple classes, and a class
    can contain multiple students.
    """

    __tablename__ = "enrollment"

    __table_args__ = (UniqueConstraint("student_id", "class_id", name="uq_student_class"),)

    id: Mapped[int] = mapped_column(primary_key=True)

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)

    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"), nullable=False)

    student: Mapped["StudentModel"] = relationship(back_populates="class_enrollments")

    class_: Mapped["ClassesModel"] = relationship(back_populates="student_enrollments")
