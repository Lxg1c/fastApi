from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    price: int


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ProductCreate(ProductBase):
    pass
