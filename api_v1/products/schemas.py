from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from api_v1.images.schemas import ImageBase


class ProductBase(BaseModel):
    name: str
    price: int


class ProductSchema(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    category_id: int
    images: Optional[List[ImageBase]] = []


class ProductCreate(ProductBase):
    images: Optional[List[ImageBase]] = []
    category_id: int


class ProductUpdate(ProductCreate):
    pass


class ProductUpdatePartial(ProductBase):
    name: str | None = None
    price: int | None = None
