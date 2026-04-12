from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
import uuid
import schemas, crud
from database import get_db, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tochka App")

@app.get("/")
def read_root():
    return {"message": "Hello World"}

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
