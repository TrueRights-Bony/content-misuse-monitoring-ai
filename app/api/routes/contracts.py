from fastapi import APIRouter, UploadFile, File
from app.services.contract_extraction import process_contract

router = APIRouter()

@router.post("/upload_contract/")
async def upload_contract(file: UploadFile = File(...)):
    content = await file.read()
    extracted_terms = process_contract(content)
    return {"message": "Contract uploaded successfully", "terms": extracted_terms}
