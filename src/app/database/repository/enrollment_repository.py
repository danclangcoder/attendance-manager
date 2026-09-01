from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.database.engine import SessionLocal
from app.database.models import EnrollmentModel, SectionModel, StudentModel

from .base_repository import BaseRepository


class EnrollmentRepository(BaseRepository[EnrollmentModel]):
    model = EnrollmentModel

    def get_students_by_class(self, class_id: int) -> Sequence[StudentModel]:
        with SessionLocal() as db:
            stmt = (
                select(StudentModel)
                .join(EnrollmentModel, EnrollmentModel.student_id == StudentModel.id)
                .where(EnrollmentModel.class_id == class_id)
                .options(joinedload(StudentModel.section).joinedload(SectionModel.course))
            )

            return db.scalars(stmt).unique().all()

    def get_by_student_and_class(self, student_id: int, class_id: int) -> EnrollmentModel | None:
        with SessionLocal() as db:
            stmt = select(EnrollmentModel).where(EnrollmentModel.student_id == student_id, EnrollmentModel.class_id == class_id)

            return db.scalars(stmt).first()

    def enroll(self, student_id: int, class_id: int) -> EnrollmentModel:
        with SessionLocal() as db:
            stmt = select(EnrollmentModel).where(EnrollmentModel.student_id == student_id, EnrollmentModel.class_id == class_id)

            existing = db.scalars(stmt).first()

            if existing:
                return existing

            enrollment = EnrollmentModel(student_id=student_id, class_id=class_id)

            db.add(enrollment)
            db.commit()
            db.refresh(enrollment)

            return enrollment

    def unenroll(self, student_id: int, class_id: int) -> bool:
        with SessionLocal() as db:
            stmt = select(EnrollmentModel).where(EnrollmentModel.student_id == student_id, EnrollmentModel.class_id == class_id)

            enrollment = db.scalars(stmt).first()

            if not enrollment:
                return False

            db.delete(enrollment)
            db.commit()

            return True

    def get_by_class(self, class_id: int) -> Sequence[EnrollmentModel]:
        with SessionLocal() as db:
            stmt = select(EnrollmentModel).where(EnrollmentModel.class_id == class_id)

            return db.scalars(stmt).all()

    def get_by_student(self, student_id: int) -> Sequence[EnrollmentModel]:
        with SessionLocal() as db:
            stmt = select(EnrollmentModel).where(EnrollmentModel.student_id == student_id)

            return db.scalars(stmt).all()

    def is_enrolled(self, student_id: int, class_id: int) -> bool:
        with SessionLocal() as db:
            stmt = select(EnrollmentModel.id).where(EnrollmentModel.student_id == student_id, EnrollmentModel.class_id == class_id)

            return db.scalar(stmt) is not None
