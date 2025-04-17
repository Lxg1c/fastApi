from pydantic import BaseModel


class CartItemBase(BaseModel):
    product_id: int
    size: str
    quantity: int


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemRead(CartItemBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
