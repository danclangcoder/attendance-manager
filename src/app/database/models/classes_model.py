from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import BaseModel
from .subject_model import SubjectModel
from .section_model import SectionModel
from .user_model import UserModel


class ClassesModel(BaseModel):
    """
    Junction table for the Subject <-> Section many-to-many relationship,
    enriched with which teacher is assigned to teach it.
    e.g. "Math, taught to Section A, by Teacher X"
    """
    __tablename__ = "classes"

    id: Mapped[int] = mapped_column(primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    section_id: Mapped[int] = mapped_column(ForeignKey("section.id"))
    # many-to-one: many classes -> one teacher
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    subject: Mapped[SubjectModel] = relationship(back_populates="classes")
    section: Mapped[SectionModel] = relationship(back_populates="classes")
    teacher: Mapped[UserModel] = relationship(back_populates="classes")
