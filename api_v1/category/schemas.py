from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    name: str


class CategorySchema(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryUpdatePartial(CategoryBase):
    name: str | None = None
