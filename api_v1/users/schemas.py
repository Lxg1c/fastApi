from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    username: Annotated[str, MinLen(3), MaxLen(20)]


class CreateUser(UserBase):
    password: bytes
    pass


class UserSchema(UserBase):
    id: int

    model_config = ConfigDict(strict=True)
