from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from api_v1.users.schemas import UserSchema
from api_v1.users.token import TokenInfo
from core.services.auth.helpers import create_access_token, create_refresh_token
from core.services.auth.validation import (
    validate_auth_user,
    get_current_token_payload,
    get_current_active_auth_user,
    get_current_auth_user_for_refresh,
)

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(http_bearer)],
)


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


@router.post(
    "/refresh/",
    response_model=TokenInfo,
    response_model_exclude_none=True,
)
def auth_refresh_jwt(
    # todo: validate user is active!!
    user: UserSchema = Depends(get_current_auth_user_for_refresh),
    # user: UserSchema = Depends(get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE)),
    # user: UserSchema = Depends(UserGetterFromToken(REFRESH_TOKEN_TYPE)),
):
    access_token = create_access_token(user)
    return TokenInfo(
        access_token=access_token,
    )


@router.get("/me/")
def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserSchema = Depends(get_current_active_auth_user),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "logged_in_at": iat,
    }