from __future__ import annotations

from datetime import date, datetime, time, timedelta
from typing import Sequence

from sqlalchemy import select

from app.database.engine import SessionLocal
from app.database.models import AttendanceRecordModel


class AttendanceRepository:
    def add_record(self, *, student_id: int, class_id: int, user_id: int, status: str = "present", qr_hash: str | None = None) -> AttendanceRecordModel:
        record = AttendanceRecordModel(student_id=student_id, class_id=class_id, user_id=user_id, status=status, qr_hash=qr_hash, scanned_at=datetime.utcnow())

        with SessionLocal() as db:
            db.add(record)
            db.commit()
            db.refresh(record)

        return record

    def get_recent(self, limit: int = 20) -> Sequence[AttendanceRecordModel]:
        with SessionLocal() as db:
            stmt = select(AttendanceRecordModel).order_by(AttendanceRecordModel.scanned_at.desc()).limit(limit)

            return db.scalars(stmt).all()

    def get_by_id(self, attendance_id: int) -> AttendanceRecordModel | None:
        with SessionLocal() as db:
            stmt = select(AttendanceRecordModel).where(AttendanceRecordModel.id == attendance_id)

            return db.scalars(stmt).first()

    def get_by_student_and_class(self, student_id: int, class_id: int):
        with SessionLocal() as db:
            stmt = (
                select(AttendanceRecordModel)
                .where(AttendanceRecordModel.student_id == student_id, AttendanceRecordModel.class_id == class_id)
                .order_by(AttendanceRecordModel.scanned_at.desc())
            )

            return db.scalars(stmt).first()

    def get_by_user(self, user_id: int) -> Sequence[AttendanceRecordModel]:
        with SessionLocal() as db:
            stmt = select(AttendanceRecordModel).where(AttendanceRecordModel.user_id == user_id).order_by(AttendanceRecordModel.scanned_at.desc())

            return db.scalars(stmt).all()

    def get_by_student_and_user(self, student_id: int, user_id: int) -> Sequence[AttendanceRecordModel]:
        with SessionLocal() as db:
            stmt = (
                select(AttendanceRecordModel)
                .where(AttendanceRecordModel.student_id == student_id, AttendanceRecordModel.user_id == user_id)
                .order_by(AttendanceRecordModel.scanned_at.desc())
            )

            return db.scalars(stmt).all()

    def get_by_qr_hash(self, qr_hash: str) -> AttendanceRecordModel | None:
        with SessionLocal() as db:
            stmt = select(AttendanceRecordModel).where(AttendanceRecordModel.qr_hash == qr_hash).order_by(AttendanceRecordModel.scanned_at.desc())

            return db.scalars(stmt).first()

    def get_by_student_and_class_and_date(self, student_id: int, class_id: int, attendance_date: date) -> AttendanceRecordModel | None:
        start = datetime.combine(attendance_date, time.min)
        end = start + timedelta(days=1)

        with SessionLocal() as db:
            stmt = (
                select(AttendanceRecordModel)
                .where(
                    AttendanceRecordModel.student_id == student_id,
                    AttendanceRecordModel.class_id == class_id,
                    AttendanceRecordModel.scanned_at >= start,
                    AttendanceRecordModel.scanned_at < end,
                )
                .order_by(AttendanceRecordModel.scanned_at.desc())
            )

            return db.scalars(stmt).first()
