from sqlalchemy import delete, select
from sqlalchemy.orm import joinedload

from app.database.engine import SessionLocal
from app.database.models import UserModel, UserSession


class UserRepository:
    @property
    def has_users(self) -> bool:
        with SessionLocal() as db:
            return db.scalar(select(UserModel.id).limit(1)) is not None

    def add_user(self, first_name, last_name, username, password, email):
        user = UserModel(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )
        with SessionLocal() as db:
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

    def create_session(self, user_id):
        with SessionLocal() as db:
            db.execute(delete(UserSession))
            db.add(UserSession(user_id=user_id))
            db.commit()

    def end_session(self):
        with SessionLocal() as db:
            db.execute(delete(UserSession))
            db.commit()

    def get_active_user(self):
        with SessionLocal() as db:
            return db.scalar(
                select(UserSession)
                .options(joinedload(UserSession.user))
            )

    def get_by_username(self, username):
        with SessionLocal() as db:
            return db.scalar(
                select(UserModel)
                .where(UserModel.username == username)
            )

    def get_by_email(self, email):
        with SessionLocal() as db:
            return db.scalar(
                select(UserModel)
                .where(UserModel.email == email)
            )