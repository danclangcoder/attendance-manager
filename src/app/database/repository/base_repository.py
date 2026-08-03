from __future__ import annotations

from typing import Any, Generic, Sequence, Type, TypeVar

from sqlalchemy import select

from app.database.engine import SessionLocal
from app.database.models import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """
    Generic CRUD repository shared by all model repositories.

    Each method opens and closes its own short-lived SessionLocal, so the
    objects it returns are safe to hand straight to UI code. Plain columns
    (e.g. `student.first_name`) stay readable after the session closes;
    relationships that weren't eagerly loaded (e.g. `section.students`)
    will raise DetachedInstanceError if touched later. Subclasses should
    add their own eager-loaded query methods for anything a treeview
    needs to display (see SectionRepository / ClassesRepository).
    """

    model: Type[ModelType]

    def get_by_id(self, id_: int) -> ModelType | None:
        with SessionLocal() as db:
            return db.get(self.model, id_)

    def get_all(self) -> Sequence[ModelType]:
        with SessionLocal() as db:
            return db.scalars(select(self.model)).all()

    def create(self, **fields: Any) -> ModelType:
        obj = self.model(**fields)
        with SessionLocal() as db:
            db.add(obj)
            db.commit()
            db.refresh(obj)
        return obj

    def update(self, id_: int, **fields: Any) -> ModelType | None:
        with SessionLocal() as db:
            obj = db.get(self.model, id_)
            if obj is None:
                return None
            for key, value in fields.items():
                setattr(obj, key, value)
            db.commit()
            db.refresh(obj)
        return obj

    def delete(self, id_: int) -> bool:
        with SessionLocal() as db:
            obj = db.get(self.model, id_)
            if obj is None:
                return False
            db.delete(obj)
            db.commit()
        return True

    def count(self) -> int:
        with SessionLocal() as db:
            return len(db.scalars(select(self.model)).all())
