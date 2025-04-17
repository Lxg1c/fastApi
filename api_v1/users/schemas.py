from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, ConfigDict


# Базовая схема пользователя
class UserBase(BaseModel):
    email: EmailStr
    username: Annotated[str, MinLen(3), MaxLen(20)]


# Схема для создания пользователя
class CreateUser(UserBase):
    password: bytes
    phone: Annotated[str, MinLen(3), MaxLen(20)]


# Схема для отображения пользователя
class UserSchema(UserBase):
    id: int
    phone: Annotated[str, MinLen(3), MaxLen(20)]
    model_config = ConfigDict(strict=True)

# Схема для обновления данных
class UserUpdate(UserBase):
    phone: Annotated[str, MinLen(3), MaxLen(20)]

# Схема для обновления данных (частично)
class UserUpdatePartial(UserBase):
    username: str | None = None
    email: EmailStr | None = None
    phone: str | None = None