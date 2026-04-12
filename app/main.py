from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

import schemas, crud
from database import get_db, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tochka App")

@app.get("/")
def read_root():
    return {"message": "Hello World"}
