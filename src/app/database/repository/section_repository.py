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
        """For a Section -> Students treeview: one query, no N+1 lazy-loads per row."""
        with SessionLocal() as db:
            stmt = select(SectionModel).options(selectinload(SectionModel.students))
            return db.scalars(stmt).unique().all()

    def get_by_name(self, name: str) -> SectionModel | None:
        with SessionLocal() as db:
            stmt = select(SectionModel).where(SectionModel.name == name)
            return db.scalars(stmt).first()
