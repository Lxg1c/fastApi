from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users.schemas import UserSchema, CreateUser
from api_v1.users.token import TokenInfo
from core.models import User
from core.models.db_helper import db_helper
from core.services.auth.helpers import create_access_token, create_refresh_token
from core.services.auth.validation import (
    validate_auth_user,
    get_current_auth_user_for_refresh,
    validate_registration,
    get_current_token_payload,
)
from core.services.shared.dependencies import get_object_by_id_or_404
from . import crud
from .crud import create_user

# Используем HTTP Bearer-авторизацию (автообработка отключена)
http_bearer = HTTPBearer(auto_error=False)

# Роутер для управления пользователями
router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(http_bearer)],
)


# Регистрация нового пользователя.
@router.post("/register/")
async def register(
        user: CreateUser = Depends(validate_registration),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):

    return await create_user(user=user, session=session)


# Аутентификация пользователя и выдача JWT access/refresh токенов.
@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
        user: UserSchema = Depends(validate_auth_user),
):

    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


# Обновление access-токена по refresh-токену.
@router.post("/refresh/", response_model=TokenInfo, response_model_exclude_none=True)
def auth_refresh_jwt(
        user: UserSchema = Depends(get_current_auth_user_for_refresh),
):

    access_token = create_access_token(user)

    return TokenInfo(
        access_token=access_token,
    )

# Получение информации о текущем пользователе по access-токену.
@router.get("/users/me/")
def auth_user_check_self_info(
        payload: dict = Depends(get_current_token_payload),
):

    return {
        "username": payload["username"],
        "email": payload["email"],
    }
