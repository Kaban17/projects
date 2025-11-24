from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Hash a plain text password using bcrypt.

    :param password: Plain text password
    :return: Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.

    :param plain_password: Plain text password
    :param hashed_password: Hashed password
    :return: True if passwords match, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)
