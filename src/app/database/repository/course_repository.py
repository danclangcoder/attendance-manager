from __future__ import annotations

from sqlalchemy import select

from app.database.engine import SessionLocal
from app.database.models import CourseModel

from .base_repository import BaseRepository


class CourseRepository(BaseRepository[CourseModel]):
    model = CourseModel

    def get_by_name(self, name: str) -> CourseModel | None:
        with SessionLocal() as db:
            stmt = select(CourseModel).where(CourseModel.name == name)
            return db.scalars(stmt).first()
