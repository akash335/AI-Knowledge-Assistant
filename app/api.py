from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import os
import shutil

from app.graph import graph
from app.retriever import build_vector_store


app = FastAPI(
    title="AI Knowledge Assistant",
    version="1.0.0",
)

UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class ChatRequest(BaseModel):
    question: str
    chat_history: list = []


@app.get("/")
def root():

    return {
        "status": "ok",
        "service": "AI Knowledge Assistant",
    }


@app.post("/chat")
def chat(request: ChatRequest):

    question = request.question.strip()

    if not question:

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    try:

        result = graph.invoke({
            "question": question,
            "chat_history": request.chat_history,
        })

        return {
            "answer": result.get(
                "answer",
                "I couldn't find that information.",
            ),
            "sources": result.get(
                "sources",
                [],
            ),
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@app.post("/upload")
async def upload(
    file: UploadFile = File(...)
):

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No file selected.",
        )

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed.",
        )

    filename = os.path.basename(
        file.filename
    )

    filepath = os.path.join(
        UPLOAD_DIR,
        filename,
    )

    if os.path.exists(filepath):

        return {
            "status": "exists",
            "filename": filename,
        }

    try:

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        build_vector_store(filepath)

        return {
            "status": "success",
            "filename": filename,
        }

    except Exception as e:

        if os.path.exists(filepath):
            os.remove(filepath)

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
