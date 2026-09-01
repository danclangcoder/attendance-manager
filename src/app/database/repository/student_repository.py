from __future__ import annotations

from sqlite3 import IntegrityError
from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.database.engine import SessionLocal
from app.database.models import SectionModel, StudentModel

from .base_repository import BaseRepository


class StudentRepository(BaseRepository[StudentModel]):
    model = StudentModel

    def get_by_section(self, section_id: int) -> Sequence[StudentModel]:
        """Students under a given section node in the treeview."""
        with SessionLocal() as db:
            stmt = select(StudentModel).where(StudentModel.section_id == section_id)
            return db.scalars(stmt).all()

    def get_all_with_section(self):
        with SessionLocal() as db:
            stmt = select(StudentModel).options(joinedload(StudentModel.section).joinedload(SectionModel.course))

            return db.scalars(stmt).unique().all()

    def get_by_student_number(self, student_number: str) -> StudentModel | None:
        with SessionLocal() as db:
            stmt = select(StudentModel).where(StudentModel.student_number == student_number)
            return db.scalars(stmt).first()

    def get_by_qr_hash(self, qr_hash: str) -> StudentModel | None:
        """Look up the student a scanned QR code is registered to.

        Attendance scans are matched against this hash (never against raw
        or parsed QR payload contents), so a QR code only marks attendance
        once it has been bound to a student via `register_qr`.
        """
        with SessionLocal() as db:
            stmt = select(StudentModel).where(StudentModel.qr_hash == qr_hash)
            return db.scalars(stmt).first()

    def register_qr(self, student_id: int, qr_hash: str) -> StudentModel | None:
        """Bind a SHA-processed QR digest to a student (QR registration)."""
        with SessionLocal() as db:
            try:
                return self.update(student_id, qr_hash=qr_hash)
            except IntegrityError:
                db.rollback()
                return None

    def is_qr_registered(self, qr_hash: str) -> bool:
        return self.get_by_qr_hash(qr_hash) is not None

    def create(self, **fields: Any) -> StudentModel | None:
        student_number = fields.get("student_number")

        if not student_number or not student_number.strip():
            return None

        if self.get_by_student_number(student_number):
            return None

        return super().create(**fields)

    def get_by_id(self, student_id: int) -> StudentModel | None:
        with SessionLocal() as db:
            stmt = select(StudentModel).where(StudentModel.id == student_id).options(joinedload(StudentModel.section).joinedload(SectionModel.course))

            return db.scalars(stmt).first()
