from sqlalchemy.orm import Mapped

from .base import Base


class Image(Base):
    __tablename__ = "images"

    product_id: Mapped[int]
    url: Mapped[str]
    is_primary: Mapped[bool]

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    def __repr__(self):
        return str(self)
