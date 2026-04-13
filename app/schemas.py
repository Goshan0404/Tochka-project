from enum import Enum


class ProductStatus(str, Enum):
    CREATED = "CREATED"
    ON_MODERATION = "ON_MODERATION"
    MODERATED = "MODERATED"
    BLOCKED = "BLOCKED"
    DELETED = "DELETED"

from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from typing import Optional, List, Any

# Базовые поля для SKU
class SKUBase(BaseModel):
    name: str
    price: int  # В моделях Integer, обычно храним в копейках/центах
    product_id: UUID
    active_quantity: int = 0
    images: List[str] = []
    characteristics: List[dict] = []

# Схема для создания (POST /api/v1/skus/)
class SKUCreate(SKUBase):
    pass

# Схема для обновления (PUT /api/v1/skus/{id})
class SKUUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    product_id: Optional[UUID] = None
    active_quantity: Optional[int] = None
    images: Optional[List[str]] = None
    characteristics: Optional[List[dict]] = None

# Схема для ответа (то, что видит клиент)
class SKUResponse(SKUBase):
    id: UUID
    
    model_config = ConfigDict(from_attributes=True)

# Ответ при загрузке картинки
class ImageUploadResponse(BaseModel):
    url: str
