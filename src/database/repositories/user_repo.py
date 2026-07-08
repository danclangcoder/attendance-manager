from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.core.utils import validator
from src.database.models import User
from src.db_config import session


class UserRepository:
    def __init__(self):
        self.session = session

    @property
    def has_users(self):
        return self.session.scalar(select(User.id).limit(1)) is not None

    def create(self, name, username, email, password, role):
        parts = name.split()
        if not name or len(parts) < 2 or any(len(chars) < 2 for chars in parts):
            return False, 'Please provide your complete name.'
        if not username or len(username) <= 4:
            return False, 'Please provide a username.'
        if not password:
            return False, 'Please provide a password.'
        if self.get_by_username(username):
            return False, 'Username is already taken.'
        if self.get_by_email(email):
            return False, 'Email is already taken.'

        self.session.add(
            User(
                name=str(name),
                username=str(username),
                email=validator.verify_email(str(email)),
                password=validator.create_password(password),
                role=role,
            )
        )

        try:
            self.session.commit()
            return True, None

        except IntegrityError as ie:
            self.session.rollback()
            return False, f'Unexpected error occured.\n{ie}'

    def get_by_username(self, username):
        return self.session.scalar(select(User).where(User.username == username))

    def get_by_email(self, email):
        return self.session.scalar(select(User).where(User.email == email))

    def get_by_id(self, user_id):
        return self.session.get(User, user_id)
