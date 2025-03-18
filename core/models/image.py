from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column
from . import Product
from .base import Base


class Image(Base):
    __tablename__ = "images"

    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    url: Mapped[str] = mapped_column(String, nullable=False)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)

    product: Mapped["Product"] = relationship("Product", back_populates="images")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, url={self.url!r})"

    def __repr__(self):
        return str(self)
