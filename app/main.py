from fastapi import FastAPI, Depends, HTTPException, Query, status, UploadFile, File
from sqlalchemy.orm import Session
from uuid import UUID
import uuid
import schemas, crud
from database import get_db, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tochka App")

@app.get("/")
def read_root():
    return {"message": "Hello World"}

# ============ Products Endpoints ============
@app.get("/api/v1/products/", response_model=schemas.PaginatedProductResponse, tags=["Products"])
def list_products(
    limit: int = Query(10, ge=0),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """Получить список всех товаров с пагинацией"""
    items, total = crud.ProductCRUD.get_paginated(db, limit=limit, offset=offset)
    return schemas.PaginatedProductResponse(
        items=items,
        total=total,
        limit=limit,
        offset=offset,
    )


@app.post(
    "/api/v1/products/",
    response_model=schemas.ProductResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Products"],
    operation_id="create_product_api_v1_products__post",
)
def create_product(
    payload: schemas.ProductCreate,
    db: Session = Depends(get_db),
):
    """Создать товар"""
    return crud.ProductCRUD.create(db, payload)


@app.get("/api/v1/products/{product_id}", response_model=schemas.ProductResponse, tags=["Products"])
def get_product(
    product_id: UUID,
    db: Session = Depends(get_db),
):
    """Получить товар по ID"""
    product = crud.ProductCRUD.get_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.put("/api/v1/products/{product_id}", response_model=schemas.ProductResponse, tags=["Products"])
def update_product(
    product_id: UUID,
    payload: schemas.ProductUpdate,
    db: Session = Depends(get_db),
):
    """Изменить товар"""
    product = crud.ProductCRUD.update(db, product_id, payload)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# ============ SKU Endpoints ============
@app.post("/api/v1/skus/", response_model=schemas.SKUResponse, status_code=status.HTTP_201_CREATED)
def create_sku(
    sku: schemas.SKUCreate,
    db: Session = Depends(get_db)
):
    """Создать SKU"""
    # Проверяем существование продукта
    product = crud.ProductCRUD.get_by_id(db, sku.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return crud.SKUCRUD.create(db, sku)

@app.put("/api/v1/skus/{sku_id}", response_model=schemas.SKUResponse)
def update_sku(
    sku_id: UUID,
    sku_update: schemas.SKUUpdate,
    db: Session = Depends(get_db)
):
    """Изменить SKU"""
    # Проверяем существование продукта
    product = crud.ProductCRUD.get_by_id(db, sku_update.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    sku = crud.SKUCRUD.update(db, sku_id, sku_update)
    if not sku:
        raise HTTPException(status_code=404, detail="SKU not found")
    
    return sku


@app.post("/api/v1/images/upload", response_model=schemas.ImageUploadResponse)
async def upload_image(
    file: UploadFile = File(...)
):
    """Загрузить изображение в S3 и получить URL"""
    # Здесь должна быть реальная логика загрузки в S3
    # Для примера генерируем фиктивный URL
    file_extension = file.filename.split(".")[-1] if file.filename else "jpg"
    file_id = uuid.uuid4()
    url = f"/s3/{file_id}.{file_extension}"
    
    # В реальном приложении здесь нужно:
    # 1. Сохранить файл в S3/MinIO
    # 2. Вернуть реальный URL
    
    return schemas.ImageUploadResponse(url=url)
