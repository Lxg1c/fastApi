from sqlalchemy.orm import Mapped

from .base import Base


class ImageModel(Base):
    product_id: Mapped[int]
    url: Mapped[str]
