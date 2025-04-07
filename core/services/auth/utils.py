import uuid
from datetime import datetime, timedelta, UTC

import bcrypt
import jwt

from core.config import settings


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None,
) -> str:
    """Кодирует JWT с подписью и временем жизни"""
    to_encode = payload.copy()
    now = datetime.now(UTC)
    expire = now + (expire_timedelta or timedelta(minutes=expire_minutes))
    to_encode.update(exp=expire, iat=now, jti=str(uuid.uuid4()))
    return jwt.encode(to_encode, private_key, algorithm=algorithm)


def decode_jwt(
        token: str | bytes,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    """Декодирует и проверяет JWT"""
    return jwt.decode(token, public_key, algorithms=[algorithm])


def hash_password(password: str) -> bytes:
    """Хэширует пароль"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def validate_password(password: str, hashed_password: bytes) -> bool:
    """Проверяет пароль по хэшу"""
    return bcrypt.checkpw(password.encode(), hashed_password)
