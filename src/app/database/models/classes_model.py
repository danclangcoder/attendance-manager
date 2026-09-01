from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.attendance_model import AttendanceRecordModel

from .base_model import BaseModel

if TYPE_CHECKING:
    from .enrollment_model import EnrollmentModel
    from .section_model import SectionModel
    from .subject_model import SubjectModel
    from .user_model import UserModel


class ClassesModel(BaseModel):
    """
    Junction table for the Subject <-> Section many-to-many relationship,
    enriched with which teacher is assigned to teach it.
    e.g. "Math, taught to Section A, by Teacher X"
    """

    __tablename__ = "classes"

    __table_args__ = (UniqueConstraint("teacher_id", "subject_id", "section_id", name="uq_teacher_subject_section"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    section_id: Mapped[int] = mapped_column(ForeignKey("section.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    subject: Mapped["SubjectModel"] = relationship(back_populates="classes")
    section: Mapped["SectionModel"] = relationship(back_populates="classes")
    teacher: Mapped["UserModel"] = relationship(back_populates="classes")
    student_enrollments: Mapped[list["EnrollmentModel"]] = relationship(back_populates="class_", cascade="all, delete-orphan")
    attendance_records: Mapped[list["AttendanceRecordModel"]] = relationship(back_populates="class_", cascade="all, delete-orphan")
