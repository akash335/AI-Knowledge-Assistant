from fastapi import APIRouter, UploadFile, File
import shutil
import os

from app.retriever import build_vector_store

router = APIRouter()

UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload(file: UploadFile = File(...)):

    filepath = os.path.join(UPLOAD_DIR, file.filename)

    # Prevent duplicate uploads
    if os.path.exists(filepath):
        return {
            "status": "exists",
            "filename": file.filename
        }

    # Save uploaded file
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Index the document
    build_vector_store(filepath)

    return {
        "status": "success",
        "filename": file.filename
    }