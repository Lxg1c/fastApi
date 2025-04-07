from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from api_v1.images.schemas import ImageBase


# Схема размера продукта
class ProductSizeSchema(BaseModel):
    size: str


# Базовая схема продукта
class ProductBase(BaseModel):
    name: str
    price: int


# Схема продукта для ответа
class ProductSchema(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    category_id: int
    description: str
    images: Optional[List[ImageBase]] = []
    sizes: List[ProductSizeSchema] = []


# Схема создания продукта
class ProductCreate(ProductBase):
    description: str
    images: Optional[List[ImageBase]] = []
    category_id: int
    sizes: List[str]


# Схема обновления продукта (полная)
class ProductUpdate(ProductCreate):
    pass


# Схема обновления продукта (частичная)
class ProductUpdatePartial(ProductBase):
    name: str | None = None
    description: str | None = None
    price: int | None = None
    sizes: Optional[List[str]] = None
