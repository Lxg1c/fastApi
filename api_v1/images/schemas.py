from pydantic import BaseModel, ConfigDict
from typing import List, Optional


# Базовая схема для Image
class ImageBase(BaseModel):
    url: str
    is_primary: bool = False


class ImageSchema(ImageBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
