import secrets
import hashlib

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette import status

security = HTTPBasic()


def hash_password(password):
    # Просто хешируем пароль
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password


def verify_password(input_password, stored_hash):
    # Проверка введенного пароля
    hashed_input_password = hashlib.sha256(input_password.encode()).hexdigest()
    return hashed_input_password == stored_hash


USER = "user"
HASHED_PASSWORD = hash_password("pass")


def authorize(credentials: HTTPBasicCredentials = Depends(security)):
    is_user_ok = secrets.compare_digest(credentials.username, USER)
    is_pass_ok = verify_password(credentials.password, HASHED_PASSWORD)

    if not (is_user_ok and is_pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password.',
            headers={'WWW-Authenticate': 'Basic'},
        )
