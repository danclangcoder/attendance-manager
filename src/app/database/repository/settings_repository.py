from sqlalchemy import select

from app.database.engine import SessionLocal
from app.database.models import AppSettings


class SettingsRepository:
    def get(self, user_id: int, key: str, default: str = "light") -> str:
        with SessionLocal() as db:
            settings = db.scalar(
                select(AppSettings).where(
                    AppSettings.user_id == user_id,
                    AppSettings.key == key,
                )
            )

            return settings.value if settings else default

    def set(self, user_id, key, value):
        with SessionLocal() as db:
            settings = db.scalar(select(AppSettings).where(AppSettings.user_id == user_id, AppSettings.key == key))

            if settings is None:
                settings = AppSettings(user_id=user_id, key=key, value=value)
                db.add(settings)
            else:
                settings.value = value

            db.commit()

    def delete(self, user_id, key):
        with SessionLocal() as db:
            settings = db.scalar(select(AppSettings).where(AppSettings.user_id == user_id, AppSettings.key == key))

            if settings is None:
                return False

            db.delete(settings)
            db.commit()
            return True
