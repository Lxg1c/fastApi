from pydantic import BaseModel


# Схема токенов доступа и обновления
class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
