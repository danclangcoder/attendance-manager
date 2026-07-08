from src.core.utils import validator


class Auth:
    def __init__(self, user_repo, session_repo):
        self.user_repo = user_repo
        self.session_repo = session_repo
        self._current_user = None

    @property
    def current_user(self):
        return self._current_user

    @property
    def is_authenticated(self):
        return self._current_user is not None

    def login(self, username, password):
        if not username or not password:
            return False, 'Username or password cannot be blank.'

        user = self.user_repo.get_by_username(username)

        if user is None:
            return False, 'Invalid user.'

        if not validator.verify_password(password, user.password):
            return False, 'Incorrect password.'

        self.session_repo.create_session(user_id=user.id)
        self._current_user = user
        return user, None

    def logout(self):
        self.session_repo.logout()
        self._current_user = None

    def restore(self):
        session = self.session_repo.get()

        if session is None:
            return False

        if session.user is None:
            self.session_repo.logout()
            return False

        self._current_user = session.user
        return True
