from pydantic import EmailStr
from sqlalchemy.orm import Mapped

from core.models import Base


class User(Base):
    __tablename__ = "users"

    email: Mapped[EmailStr]
    username: Mapped[str]
    hashed_password: Mapped[bytes]
