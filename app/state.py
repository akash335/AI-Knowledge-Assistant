from typing import TypedDict

class GraphState(TypedDict):
    question: str
    documents: list
    answer: str