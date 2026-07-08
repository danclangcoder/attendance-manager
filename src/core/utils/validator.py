import bcrypt
import email_validator as em
from email_validator import EmailNotValidError


def verify_email(email):
    try:
        valid = em.validate_email(email)
        return valid.email
    except EmailNotValidError:
        return None


def create_password(password):
    return bcrypt.hashpw(password=password.encode('utf-8'), salt=bcrypt.gensalt())


def verify_password(password, hash):
    return bcrypt.checkpw(password.encode('utf-8'), hash)
