from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base


class User(Base):
    __tablename__ = "users"

    # Email пользователя. Обязательное поле, уникальное.
    email: Mapped[str] = mapped_column(
        nullable=False,
        unique=True,
    )

    # Телефон пользователя. Обязательное поле, уникальное.
    phone: Mapped[str] = mapped_column(
        nullable=False,
        unique=True,
        server_default="''",
    )

    # Имя пользователя (username). Обязательное поле, уникальное.
    username: Mapped[str] = mapped_column(
        nullable=False,
        unique=True,
    )

    # Пароль в зашифрованном виде (hash). Храним в байтах.
    password: Mapped[bytes]

    # Человеко-читаемое представление модели
    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username!r})"

    def __repr__(self):
        return str(self)
