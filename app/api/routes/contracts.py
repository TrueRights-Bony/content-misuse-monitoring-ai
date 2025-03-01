from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
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

    # Check if the file already exists in the database
    existing_contract = db.query(Contract).filter(Contract.filename == file.filename).first()
    
    if existing_contract:
        raise HTTPException(status_code=400, detail="Contract already exists")

    # Save the uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Add new contract entry
    contract = Contract(filename=file.filename)
    db.add(contract)
    db.commit()

    return {"message": "Contract uploaded successfully", "filename": file.filename}

@router.get("/list")
async def list_contracts(db: Session = Depends(get_db)):
    contracts = db.query(Contract).all()
    return {"contracts": [{"id": c.id, "filename": c.filename, "status": c.status} for c in contracts]}