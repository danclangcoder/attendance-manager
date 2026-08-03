from __future__ import annotations

from sqlalchemy import select

from app.database.engine import SessionLocal
from app.database.models import SubjectModel

from .base_repository import BaseRepository


class SubjectRepository(BaseRepository[SubjectModel]):
    model = SubjectModel

    def get_by_code(self, code: str) -> SubjectModel | None:
        with SessionLocal() as db:
            stmt = select(SubjectModel).where(SubjectModel.code == code)
            return db.scalars(stmt).first()
