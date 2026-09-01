from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import BaseModel

if TYPE_CHECKING:
    from .classes_model import ClassesModel
    from .student_model import StudentModel
    from .user_model import UserModel


class AttendanceRecordModel(BaseModel):
    __tablename__ = "attendance_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="present")
    scanned_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    qr_hash: Mapped[str | None] = mapped_column(String(128), default=None)

    student: Mapped["StudentModel"] = relationship(back_populates="attendance_records")
    user: Mapped["UserModel"] = relationship(back_populates="attendance_records")
    class_: Mapped["ClassesModel"] = relationship(back_populates="attendance_records")
