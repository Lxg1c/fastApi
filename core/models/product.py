from sqlalchemy.orm import Mapped
from .base import Base


class Product(Base):
    __tablename__ = "products"

    name: Mapped[str]
    price: Mapped[int]

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"

    def __repr__(self):
        return str(self)
