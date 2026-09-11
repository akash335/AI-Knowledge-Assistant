from fastapi import APIRouter

from app.document_manager import (
    list_documents,
    delete_document,
    rebuild_vector_store,
)

router = APIRouter()


@router.get("/documents")
def documents():
    return list_documents()


@router.delete("/documents/{filename}")
def delete(filename: str):

    delete_document(filename)

    rebuild_vector_store()

    return {
        "success": True
    }