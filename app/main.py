from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

import schemas, crud
from database import get_db, engine
import models
from uuid import UUID

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tochka App")

@app.get("/")
def read_root():
    return {"message": "Hello World"}

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