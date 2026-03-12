from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(default_password: str, hashed_password: str) -> bool:
    """
    Проверка введенного пароля с тем что захэширован в таблице
    """
    return pwd_context.verify(default_password, hashed_password)

def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)