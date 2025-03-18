from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column
from .base import Base


class Product(Base):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)

    images: Mapped[list["Image"]] = relationship(
        "Image", back_populates="product", cascade="all, delete-orphan"
    )
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("categorys.id"), nullable=False
    )
    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="products",
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"

    def __repr__(self):
        return str(self)
