from fastapi import Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.users.crud import get_user_by_username
from api_v1.users.schemas import UserSchema
from . import utils as auth_utils
from .helpers import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from ...models.db_helper import db_helper

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/users/login/",
)


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
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
        validate_token_type(payload, token_type)
        return await get_user_by_token_sub(payload)

    return get_auth_user_from_token


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    def __call__(
        self,
        payload: dict = Depends(get_current_token_payload),
    ):
        validate_token_type(payload, self.token_type)
        return get_user_by_token_sub(payload)


get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)


def get_current_active_auth_user(
    user: UserSchema = Depends(get_current_auth_user),
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="inactive user",
    )


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    unauthorized_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )

    user = await get_user_by_username(username=username, session=session)
    if not user:
        raise unauthorized_exc

    if not auth_utils.validate_password(
        password=password,
        hashed_password=user.password,
    ):
        raise unauthorized_exc

    return user
