from fastapi import Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.users.crud import get_user_by_username, get_user_by_email
from api_v1.users.schemas import UserSchema, CreateUser
from . import utils as auth_utils
from .helpers import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from .utils import hash_password
from ...models.db_helper import db_helper

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/users/login/",
)


def get_current_token_payload(
        token: str = Depends(oauth2_scheme),
) -> dict:
    """Декодирует JWT, возвращает payload"""
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


def validate_token_type(
        payload: dict,
        token_type: str,
) -> bool:
    """Проверка типа токена"""
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} expected {token_type!r}",
    )


async def get_user_by_token_sub(
        payload: dict, session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> UserSchema:
    """Получение пользователя из токена"""
    username: str | None = payload.get("sub")

    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token (no subject found)",
        )

    user = await get_user_by_username(username=username, session=session)

    if user:
        return UserSchema.model_validate(user)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token (user not found)",
    )


def get_auth_user_from_token_of_type(token_type: str):
    async def get_auth_user_from_token(
            payload: dict = Depends(get_current_token_payload),
    ) -> UserSchema:
        """Фабрика зависимостей по типу токена"""
        validate_token_type(payload, token_type)
        return await get_user_by_token_sub(payload)

    return get_auth_user_from_token


class UserGetterFromToken:
    """Класс-зависимость для получения пользователя по токену"""

    def __init__(self, token_type: str):
        self.token_type = token_type

    def __call__(
            self,
            payload: dict = Depends(get_current_token_payload),
    ):
        validate_token_type(payload, self.token_type)
        return get_user_by_token_sub(payload)


# Зависимости
get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)


async def validate_registration(
        username: str = Form(),
        email: EmailStr = Form(),
        phone: str = Form(),
        password: str = Form(),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> CreateUser:
    """Валидация регистрации и хэширование пароля"""
    user = await get_user_by_username(username=username, session=session)

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is already registered",
        )

    user = await get_user_by_email(email=email, session=session)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        )

    password = hash_password(password=password)

    return CreateUser(username=username, email=email, password=password, phone=phone)


async def validate_auth_user(
        email: EmailStr = Form(),
        password: str = Form(),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Проверка email и пароля при логине"""
    unauthorized_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid email or password",
    )

    user = await get_user_by_email(email=email, session=session)
    if not user:
        raise unauthorized_exc

    if not auth_utils.validate_password(
            password=password,
            hashed_password=user.password,
    ):
        raise unauthorized_exc

    return user
