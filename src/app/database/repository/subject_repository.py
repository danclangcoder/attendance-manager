from __future__ import annotations

from sqlalchemy import select

from app.database.engine import SessionLocal
from app.database.models import SubjectModel

from .base_repository import BaseRepository


class SubjectRepository(BaseRepository[SubjectModel]):
    model = SubjectModel

    def get_by_name(self, name: str) -> SubjectModel | None:
        with SessionLocal() as db:
            stmt = select(SubjectModel).where(SubjectModel.name == name)
            return db.scalars(stmt).first()
