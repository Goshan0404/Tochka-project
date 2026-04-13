from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field

try:
    # pydantic v2
    from pydantic import ConfigDict  # type: ignore
except Exception:  # pragma: no cover
    ConfigDict = None  # type: ignore


class ORMBaseModel(BaseModel):
    """Base model with ORM support (pydantic v1/v2 compatible)."""

    if ConfigDict is not None:  # pydantic v2
        model_config = ConfigDict(from_attributes=True)
    else:  # pydantic v1
        class Config:
            orm_mode = True


# -------- Images --------

class ImageUploadResponse(ORMBaseModel):
    url: str


class ImageUpload(ORMBaseModel):
    # Для multipart/form-data в FastAPI обычно используют UploadFile,
    # но в OpenAPI схема описана как binary, поэтому здесь bytes.
    file: bytes


class Image(ORMBaseModel):
    url: str
    ordering: int


# -------- Categories --------

class CategoryCreate(ORMBaseModel):
    name: str
    parent_id: Optional[UUID] = None


class CategoryUpdate(ORMBaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None


class CategoryRef(ORMBaseModel):
    id: UUID
    name: str
    level: int
    path: str


class CategoryResponse(ORMBaseModel):
    name: str
    id: UUID
    level: int
    path: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


# -------- Products / SKU --------

class ProductStatus(str, Enum):
    CREATED = "CREATED"
    ON_MODERATION = "ON_MODERATION"
    MODERATED = "MODERATED"
    BLOCKED = "BLOCKED"
    DELETED = "DELETED"


class SKUCreate(ORMBaseModel):
    name: str
    price: int
    active_quantity: int = 0
    images: list[Image] = Field(default_factory=list)
    characteristics: list[dict[str, Any]] = Field(default_factory=list)
    product_id: UUID


class SKUUpdate(ORMBaseModel):
    name: str
    price: int
    active_quantity: int
    images: list[Image] = Field(default_factory=list)
    characteristics: list[dict[str, Any]] = Field(default_factory=list)
    product_id: UUID


class SKUResponse(ORMBaseModel):
    name: str
    price: int
    active_quantity: int = 0
    images: list[Image] = Field(default_factory=list)
    characteristics: list[dict[str, Any]] = Field(default_factory=list)
    product_id: UUID

    id: UUID
    created_at: datetime
    updated_at: datetime


class ProductCreate(ORMBaseModel):
    title: str
    description: Optional[str] = None
    images: list[Image] = Field(default_factory=list)
    characteristics: list[dict[str, Any]] = Field(default_factory=list)
    category_id: UUID


class ProductUpdate(ORMBaseModel):
    title: str
    description: Optional[str] = None
    images: list[Image] = Field(default_factory=list)
    characteristics: list[dict[str, Any]] = Field(default_factory=list)
    category_id: UUID


class ProductResponse(ORMBaseModel):
    title: str
    description: Optional[str] = None
    status: ProductStatus = ProductStatus.CREATED
    images: list[Image] = Field(default_factory=list)
    characteristics: list[dict[str, Any]] = Field(default_factory=list)

    id: UUID
    created_at: datetime
    updated_at: datetime
    category: CategoryRef
    skus: list[SKUResponse]


class PaginatedProductResponse(ORMBaseModel):
    items: list[ProductResponse]
    total: int
    limit: int
    offset: int


# -------- Validation errors (FastAPI style) --------

class ValidationError(ORMBaseModel):
    loc: list[str | int]
    msg: str
    type: str
    input: Any = None
    ctx: dict[str, Any] = Field(default_factory=dict)


class HTTPValidationError(ORMBaseModel):
    detail: list[ValidationError] = Field(default_factory=list)