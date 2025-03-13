from sqlalchemy.orm import Mapped, mapped_column
from core.models import Base


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        nullable=False,
        unique=True,
    )
    username: Mapped[str] = mapped_column(
        nullable=False,
        unique=True,
    )
    password: Mapped[bytes]

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username!r})"

    def __repr__(self):
        return str(self)
