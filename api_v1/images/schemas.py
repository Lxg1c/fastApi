from pydantic import BaseModel, ConfigDict


# Базовая схема изображения
class ImageBase(BaseModel):
    url: str
    is_primary: bool = False


# Схема изображения для ответа
class ImageSchema(ImageBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
