from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database.engine import SessionLocal
from app.database.models import SectionModel

from .base_repository import BaseRepository


class SectionRepository(BaseRepository[SectionModel]):
    model = SectionModel

    def get_all_with_students(self) -> Sequence[SectionModel]:
        with SessionLocal() as db:
            stmt = select(SectionModel).options(selectinload(SectionModel.students), selectinload(SectionModel.course))

            return db.scalars(stmt).unique().all()

    def get_by_name(self, name: str) -> SectionModel | None:
        with SessionLocal() as db:
            stmt = select(SectionModel).where(SectionModel.name == name)
            return db.scalars(stmt).first()

    def get_by_course(self, course_id):
        with SessionLocal() as db:
            stmt = select(SectionModel).where(SectionModel.course_id == course_id)
            return db.scalars(stmt).unique().all()

    def get_by_course_and_name(self, course_id: int, name: str) -> SectionModel | None:
        with SessionLocal() as db:
            stmt = select(SectionModel).where(SectionModel.course_id == course_id, SectionModel.name == name)
            return db.scalars(stmt).first()

    def get_by_course_and_year(self, course_id, year_level):
        with SessionLocal() as db:
            return db.scalars(select(SectionModel).where(SectionModel.course_id == course_id, SectionModel.year_level == year_level)).all()
