from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from .base import Base


class Image(Base):
    __tablename__ = "images"

    # Внешний ключ на продукт, при удалении продукта — удаляются изображения
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )

    # URL изображения
    url: Mapped[str] = mapped_column(String, nullable=False)

    # Является ли изображение основным (например, отображается первым)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)

    # Связь с моделью Product, обратная связь — images
    product: Mapped["Product"] = relationship("Product", back_populates="images")

    # Для удобства вывода в консоль
    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, url={self.url!r})"

    def __repr__(self):
        return str(self)
