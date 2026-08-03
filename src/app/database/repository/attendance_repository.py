from __future__ import annotations

from datetime import datetime
from typing import Sequence

from sqlalchemy import select

from app.database.engine import SessionLocal
from app.database.models import AttendanceRecordModel


class AttendanceRepository:
    def add_record(self, *, student_id: int, user_id: int, status: str = "present", qr_hash: str | None = None) -> AttendanceRecordModel:
        record = AttendanceRecordModel(student_id=student_id, user_id=user_id, status=status, qr_hash=qr_hash, scanned_at=datetime.utcnow())
        with SessionLocal() as db:
            db.add(record)
            db.commit()
            db.refresh(record)
        return record

    def get_recent(self, limit: int = 20) -> Sequence[AttendanceRecordModel]:
        with SessionLocal() as db:
            stmt = select(AttendanceRecordModel).order_by(AttendanceRecordModel.scanned_at.desc()).limit(limit)
            return db.scalars(stmt).all()
