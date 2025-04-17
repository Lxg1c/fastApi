from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users.schemas import UserSchema, CreateUser, UserUpdate, UserUpdatePartial
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
@router.get("/me/")
def auth_user_check_self_info(
        payload: dict = Depends(get_current_token_payload),
):

    return {
        "id": payload["id"],
        "username": payload["username"],
        "email": payload["email"],
        "phone": payload["phone"],
    }

# Удаление пользователя по ID.
@router.delete("/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user: User = Depends(get_object_by_id_or_404(
            model=User,
            id_name="user_id",
            get_func=crud.get_user_by_id
        )),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):

    try:
        await crud.delete_user(user=user, session=session)
        return {
                "message": "User deleted",
        }
    except Exception as err:
        # Возможные ошибки (например, нарушение внешнего ключа)
        return {
            "message": "Error when deleting user",
            "error": str(err),
        }

# Полное обновление продукта
@router.put("/{user_id}", response_model=UserSchema)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await crud.get_user_by_id(session=session, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return await crud.update_user(
        session=session, user=user, user_update=user_update, partial=False
    )


# Частичное обновление продукта
@router.patch("/{user_id}", response_model=UserSchema)
async def update_user_partial(
    user_id: int,
    user_update: UserUpdatePartial,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await crud.get_user_by_id(session=session, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return await crud.update_user(
        session=session, user=user, user_update=user_update, partial=True
    )