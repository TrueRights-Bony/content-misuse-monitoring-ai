from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.models.base import SessionLocal
from app.models.contract import Contract
import os
import shutil

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload_contract/")
async def upload_contract(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    contract = Contract(filename=file.filename)
    db.add(contract)
    db.commit()
    
    return {"message": "Contract uploaded successfully", "filename": file.filename}
