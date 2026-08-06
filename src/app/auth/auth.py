import bcrypt
import email_validator
from email_validator import EmailNotValidError


class Auth:
    def __init__(self, user_repo):
        self.user_repo = user_repo
        self.active_user = None

    def register(self, first_name, middle_name, last_name, username, password, email: str | None):
        fields = (
            (self.validate_first_name, first_name),
            (self.validate_middle_name, middle_name),
            (self.validate_last_name, last_name),
            (self.validate_username, username),
            (self.validate_email, email),
            (self.validate_password, password),
        )

        for validate, value in fields:
            success, message = validate(value)
            if not success:
                return False, message

        if self.user_repo.get_by_username(username):
            return False, "Username is already taken."
        if self.user_repo.get_by_email(email):
            return False, "Email is already taken."

        user = self.user_repo.add_user(
            first_name,
            middle_name,
            last_name,
            username,
            password=self.create_password(password),
            email=email,
        )
        
        self.user_repo.create_session(user_id=user.id)
        self.active_user = user
        return True, None

    def login(self, username, password):
        user = self.user_repo.get_by_username(username)
        if user is None:
            return False, "Invalid username."
        if not self.verify_password(password, user.password):
            return False, "Incorrect password."
        self.user_repo.create_session(user_id=user.id)
        self.active_user = user
        return True, None

    def restore_session(self):
        active_session = self.user_repo.get_active_user()
        if active_session:
            self.active_user = active_session.user
            return True
        else:
            self.user_repo.end_session()
            return False

    def logout(self):
        self.user_repo.end_session()
        self.active_user = None

    @property
    def is_logged_in(self) -> bool:
        session = self.restore_session()
        return session

    @staticmethod
    def create_password(password):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def verify_password(password, hash_str):
        return bcrypt.checkpw(password.encode("utf-8"), hash_str.encode("utf-8"))

    @staticmethod
    def validate_first_name(first_name):
        if len(first_name.strip()) < 2:
            return False, "Please provide your complete name."
        return True, None

    @staticmethod
    def validate_middle_name(middle_name):
        if middle_name and len(middle_name.strip()) < 2:
            return False, "Please provide your complete middle name."
        return True, None

    @staticmethod
    def validate_last_name(last_name):
        if len(last_name.strip()) < 2:
            return False, "Please provide your complete name."
        return True, None

    @staticmethod
    def validate_username(username):
        if len(username.strip()) < 5:
            return False, "Username must be at least 5 characters and above."
        return True, None

    @staticmethod
    def validate_email(email):
        if not email:
            return True, None
        try:
            email_validator.validate_email(email)
            return True, None
        except EmailNotValidError:
            return False, "Invalid email address."

    @staticmethod
    def validate_password(password):
        if len(password.strip()) < 5:
            return False, "Password must be at least 5 characters and above."
        return True, None
