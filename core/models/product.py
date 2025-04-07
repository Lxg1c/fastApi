from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from .base import Base


class ProductSize(Base):
    __tablename__ = "product_sizes"

    # Первичный ключ
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Внешний ключ на продукт
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)

    # Размер (например, "S", "M", "L", "42", "10.5" и т.д.)
    size: Mapped[str] = mapped_column(String, nullable=False)

    # Связь с продуктом (обратная связь настроена в Product)
    product: Mapped["Product"] = relationship("Product", back_populates="sizes")


class Product(Base):
    __tablename__ = "products"

    # Название продукта
    name: Mapped[str] = mapped_column(String, nullable=False)

    # Цена продукта
    price: Mapped[int] = mapped_column(Integer, nullable=False)

    # Описание продукта (необязательное)
    description: Mapped[str] = mapped_column(String, nullable=True)

    # Связь с размерами (один продукт — много размеров)
    sizes: Mapped[list["ProductSize"]] = relationship(
        "ProductSize", back_populates="product", cascade="all, delete-orphan"
    )

    # Связь с изображениями продукта
    images: Mapped[list["Image"]] = relationship(
        "Image", back_populates="product", cascade="all, delete-orphan"
    )

    # Внешний ключ на категорию
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("categorys.id"), nullable=False  # ❗️Опечатка в "categorys"
    )

    # Связь с категорией
    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="products",
    )

    # Строковое представление объекта
    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"

    def __repr__(self):
        return str(self)
