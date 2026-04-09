from sqlalchemy import (
    Column, String, Integer, Boolean, DateTime, ForeignKey,
    JSON, Enum as SQLEnum, Index
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import uuid
import enum


class ProductStatusEnum(str, enum.Enum):
    CREATED = "CREATED"
    ON_MODERATION = "ON_MODERATION"
    MODERATED = "MODERATED"
    BLOCKED = "BLOCKED"
    DELETED = "DELETED"


class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    level = Column(Integer, nullable=False, default=0)
    path = Column(String, nullable=False, default="")
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    parent = relationship("Category", remote_side=[id], backref="children")
    products = relationship("Product", back_populates="category")

    __table_args__ = (
        Index('idx_category_path', 'path'),
        Index('idx_category_parent_id', 'parent_id'),
    )


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(SQLEnum(ProductStatusEnum), nullable=False, default=ProductStatusEnum.CREATED)
    images = Column(JSON, nullable=False, default=list)
    characteristics = Column(JSON, nullable=False, default=list)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    category = relationship("Category", back_populates="products")
    skus = relationship("SKU", back_populates="product", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_product_category_id', 'category_id'),
        Index('idx_product_status', 'status'),
        Index('idx_product_created_at', 'created_at'),
    )


class SKU(Base):
    __tablename__ = "skus"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    active_quantity = Column(Integer, nullable=False, default=0)
    images = Column(JSON, nullable=False, default=list)
    characteristics = Column(JSON, nullable=False, default=list)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    product = relationship("Product", back_populates="skus")

    __table_args__ = (
        Index('idx_sku_product_id', 'product_id'),
        Index('idx_sku_price', 'price'),
    )