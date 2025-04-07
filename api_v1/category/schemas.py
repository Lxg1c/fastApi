from pydantic import BaseModel, ConfigDict


# Базовая схема категории, используется как основа для других
class CategoryBase(BaseModel):
    name: str  # Название категории


# Схема, которая возвращается клиенту
class CategorySchema(CategoryBase):
    # Разрешаем создание схемы из ORM-объектов (SQLAlchemy моделей)
    model_config = ConfigDict(from_attributes=True)
    id: int  # Уникальный идентификатор категории


# Схема для создания новой категории
class CategoryCreate(CategoryBase):
    pass


# Схема для полного обновления категории
class CategoryUpdate(CategoryBase):
    pass


# Схема для частичного обновления категории
class CategoryUpdatePartial(CategoryBase):
    name: str | None = None
