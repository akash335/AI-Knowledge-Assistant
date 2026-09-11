from fastapi import FastAPI
from pydantic import BaseModel
from backend.api.upload import router as upload_router
from app.graph import graph
from backend.api.documents import router as documents_router
app.include_router(documents_router)

app = FastAPI(
    title="AI Knowledge Assistant",
    version="1.0.0"
)
app.include_router(upload_router)

class ChatRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "AI Knowledge Assistant API Running"
    }


@app.post("/chat")
def chat(req: ChatRequest):

    result = graph.invoke(
        {
            "question": req.question
        }
    )

    return {
        "answer": result["answer"],
        "sources": result["sources"]
    }