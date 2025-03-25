from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from api_v1.images.schemas import ImageBase


class ProductSizeSchema(BaseModel):
    size: str


class ProductBase(BaseModel):
    name: str
    price: int


class ProductSchema(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    category_id: int
    description: str
    images: Optional[List[ImageBase]] = []
    sizes: List[ProductSizeSchema] = []


class ProductCreate(ProductBase):
    description: str
    images: Optional[List[ImageBase]] = []
    category_id: int
    sizes: List[str]


class ProductUpdate(ProductCreate):
    pass


class ProductUpdatePartial(ProductBase):
    name: str | None = None
    description: str | None = None
    price: int | None = None
    sizes: Optional[List[str]] = None
