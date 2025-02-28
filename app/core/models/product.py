from sqlalchemy.orm import Mapped
from app.core.models.base import BaseModel


class Product(BaseModel):
    name: Mapped[str]
    price: Mapped[int]
