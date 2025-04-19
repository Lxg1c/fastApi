from pydantic import BaseModel


class FavoriteItemBase(BaseModel):
    product_id: int


class FavoriteItemCreate(FavoriteItemBase):
    pass


class FavoriteItemUpdate(BaseModel):
    quantity: int


class FavoriteItemRead(FavoriteItemBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
