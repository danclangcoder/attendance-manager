import json

from google.oauth2.credentials import Credentials
from sqlalchemy import delete, select

from app.database.engine import SessionLocal
from app.database.models import GoogleAccount


class GoogleAccountRepository:
    def get_by_user_id(self, user_id):
        with SessionLocal() as db:
            return db.scalar(select(GoogleAccount).where(GoogleAccount.user_id == user_id))

    def get_by_google_id(self, google_id):
        with SessionLocal() as db:
            return db.scalar(select(GoogleAccount).where(GoogleAccount.google_id == google_id))

    def save(self, user_id, google_id, email, name, credentials):
        with SessionLocal() as db:
            account = db.scalar(select(GoogleAccount).where(GoogleAccount.user_id == user_id))

            if account is None:
                account = GoogleAccount(user_id=user_id, google_id=google_id, email=email, name=name, credentials=credentials.to_json())
                db.add(account)
            else:
                account.google_id = google_id
                account.email = email
                account.name = name
                account.credentials = credentials.to_json()

            db.commit()
            db.refresh(account)
            return account

    def unlink(self, user_id):
        with SessionLocal() as db:
            db.execute(delete(GoogleAccount).where(GoogleAccount.user_id == user_id))
            db.commit()

    def get_credentials(self, user_id: int) -> Credentials | None:
        account = self.get_by_user_id(user_id)

        if account is None or account.credentials is None:
            return None

        return Credentials.from_authorized_user_info(json.loads(account.credentials))

    def update_credentials(self, user_id: int, credentials: Credentials):
        with SessionLocal() as db:
            account = db.scalar(select(GoogleAccount).where(GoogleAccount.user_id == user_id))

            if account is None:
                return

            account.credentials = credentials.to_json()
            db.commit()
