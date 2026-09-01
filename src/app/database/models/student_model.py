from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import BaseModel

if TYPE_CHECKING:
    from .attendance_model import AttendanceRecordModel
    from .enrollment_model import EnrollmentModel
    from .section_model import SectionModel


class StudentModel(BaseModel):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    student_number: Mapped[str] = mapped_column(String(16), unique=True, nullable=False)
    qr_hash: Mapped[str | None] = mapped_column(String(128), default=None, unique=True)
    section_id: Mapped[int] = mapped_column(ForeignKey("section.id"))

    # many-to-one: many students -> one section
    section: Mapped["SectionModel"] = relationship(back_populates="students")
    class_enrollments: Mapped[list["EnrollmentModel"]] = relationship(back_populates="student", cascade="all, delete-orphan")
    attendance_records: Mapped[list["AttendanceRecordModel"]] = relationship(back_populates="student", cascade="all, delete-orphan")
