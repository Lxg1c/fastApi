from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Category(Base):
    __tablename__ = "categorys"  # Название таблицы в базе данных

    # Название категории (уникальное и обязательное поле)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    # Связь один-ко-многим: у одной категории может быть много продуктов
    products: Mapped[list["Product"]] = relationship(
        "Product",  # Название связанной модели
        back_populates="category"  # Обратная связь из модели Product
    )

    def __str__(self):
        # Человеко-читаемое строковое представление объекта (например, для логов)
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"

    def __repr__(self):
        # Представление объекта, используемое в интерпретаторе/отладке
        return str(self)
