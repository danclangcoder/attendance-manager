from sqlalchemy import delete, select

from src.db_config import session
from src.database.models import CurrentSession


class SessionRepository:
    def create_session(self, user_id):
        session.execute(delete(CurrentSession))
        session.add(CurrentSession(user_id=user_id))
        session.commit()

    def get(self):
        return session.scalar(select(CurrentSession))

    def logout(self):
        session.execute(delete(CurrentSession))
        session.commit()
