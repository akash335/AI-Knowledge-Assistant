from typing import TypedDict
from langchain_core.documents import Document


class GraphState(TypedDict):
    question: str
    documents: list[Document]
    answer: str
    sources: list
    chat_history: list
