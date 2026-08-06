from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.database.engine import SessionLocal
from app.database.models import ClassesModel

from .base_repository import BaseRepository


class ClassesRepository(BaseRepository[ClassesModel]):
    model = ClassesModel

    def exists(self, teacher_id: int, subject_id: int, section_id: int) -> bool:
        with SessionLocal() as db:
            return db.scalar(
                select(ClassesModel.id).where(
                    ClassesModel.teacher_id == teacher_id,
                    ClassesModel.subject_id == subject_id,
                    ClassesModel.section_id == section_id,
                )
            ) is not None

    def get_all_detailed(self) -> Sequence[ClassesModel]:
        """
        One row per class assignment with subject, section, and teacher
        already loaded — e.g. for a flat treeview row like
        'Math 101 - Section A - Mr. Reyes'.
        """
        with SessionLocal() as db:
            stmt = select(ClassesModel).options(
                joinedload(ClassesModel.subject),
                joinedload(ClassesModel.section),
                joinedload(ClassesModel.teacher),
            )
            return db.scalars(stmt).unique().all()

    def get_by_teacher(self, teacher_id: int) -> Sequence[ClassesModel]:
        """For a Teacher -> Classes treeview branch."""
        with SessionLocal() as db:
            stmt = (
                select(ClassesModel)
                .where(ClassesModel.teacher_id == teacher_id)
                .options(joinedload(ClassesModel.subject), joinedload(ClassesModel.section))
            )
            return db.scalars(stmt).unique().all()

    def get_by_section(self, section_id: int) -> Sequence[ClassesModel]:
        """For a Section -> Subjects/Classes treeview branch."""
        with SessionLocal() as db:
            stmt = (
                select(ClassesModel)
                .where(ClassesModel.section_id == section_id)
                .options(joinedload(ClassesModel.subject), joinedload(ClassesModel.teacher))
            )
            return db.scalars(stmt).unique().all()

    def get_by_subject(self, subject_id: int) -> Sequence[ClassesModel]:
        """For a Subject -> Class treeview."""
        with SessionLocal() as db:
            stmt = (
                select(ClassesModel)
                .where(ClassesModel.subject_id == subject_id)
                .options(joinedload(ClassesModel.subject))
            )
            return db.scalars(stmt).unique().all()
