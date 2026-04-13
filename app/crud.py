from typing import Optional
from uuid import UUID, uuid4

from fastapi import HTTPException
from sqlalchemy.orm import Session, selectinload

from fastapi.encoders import jsonable_encoder
import models
import schemas

class CategoryCRUD:
    @staticmethod
    def get_by_id(db: Session, category_id: UUID) -> Optional[models.Category]:
        return db.query(models.Category).filter(models.Category.id == category_id).first()


class ProductCRUD:
    @staticmethod
    def _to_product_response(product: models.Product) -> schemas.ProductResponse:
        if product.category is None:
            # при nullable=False на FK этого быть не должно, но на всякий случай
            raise HTTPException(status_code=500, detail="Product category is not loaded")

        return schemas.ProductResponse(
            id=product.id,
            title=product.title,
            description=product.description,
            status=product.status.value if hasattr(product.status, "value") else product.status,
            images=product.images or [],
            characteristics=product.characteristics or [],
            created_at=product.created_at,
            # updated_at у вас без server_default, поэтому гарантируем не-None
            updated_at=product.updated_at or product.created_at,
            category=schemas.CategoryRef(
                id=product.category.id,
                name=product.category.name,
                level=product.category.level,
                path=product.category.path,
            ),
            skus=[
                schemas.SKUResponse(
                    id=sku.id,
                    name=sku.name,
                    price=sku.price,
                    active_quantity=sku.active_quantity,
                    images=sku.images or [],
                    characteristics=sku.characteristics or [],
                    product_id=sku.product_id,
                    created_at=sku.created_at,
                    updated_at=sku.updated_at or sku.created_at,
                )
                for sku in (product.skus or [])
            ],
        )

    @staticmethod
    def get_paginated(
        db: Session,
        limit: int = 10,
        offset: int = 0,
    ) -> tuple[list[schemas.ProductResponse], int]:
        base_q = db.query(models.Product)
        total = base_q.count()

        products = (
            base_q.options(
                selectinload(models.Product.category),
                selectinload(models.Product.skus),
            )
            .order_by(models.Product.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        return [ProductCRUD._to_product_response(p) for p in products], total

    @staticmethod
    def get_by_id(db: Session, product_id: UUID) -> Optional[schemas.ProductResponse]:
        product = (
            db.query(models.Product)
            .options(
                selectinload(models.Product.category),
                selectinload(models.Product.skus),
            )
            .filter(models.Product.id == product_id)
            .first()
        )
        if not product:
            return None
        return ProductCRUD._to_product_response(product)

    @staticmethod
    def create(db: Session, payload: schemas.ProductCreate) -> schemas.ProductResponse:
        category = CategoryCRUD.get_by_id(db, payload.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        product = models.Product(
            title=payload.title,
            description=payload.description,
            category_id=payload.category_id,
            status=models.ProductStatusEnum.CREATED,
            images=jsonable_encoder(payload.images or []),
            characteristics=jsonable_encoder(payload.characteristics or []),
            # created_at проставится server_default=func.now()
            # updated_at у вас только onupdate, поэтому на insert будет NULL -> ставим вручную
            updated_at=None,
        )

        db.add(product)
        db.commit()
        db.refresh(product)

        # подгрузить связи и собрать ProductResponse
        return ProductCRUD.get_by_id(db, product.id)  # type: ignore[return-value]

    @staticmethod
    def update(
        db: Session,
        product_id: UUID,
        payload: schemas.ProductUpdate,
    ) -> Optional[schemas.ProductResponse]:
        product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if not product:
            return None

        category = CategoryCRUD.get_by_id(db, payload.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        product.title = payload.title
        product.description = payload.description
        product.category_id = payload.category_id
        product.images = jsonable_encoder(payload.images or [])
        product.characteristics = jsonable_encoder(payload.characteristics or [])
        # updated_at сам проставится onupdate=func.now() при UPDATE
        # но чтобы не было NULL, если по какой-то причине onupdate не сработал:
        if product.updated_at is None:
            product.updated_at = product.created_at

        db.commit()
        db.refresh(product)

        return ProductCRUD.get_by_id(db, product_id)