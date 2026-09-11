from langgraph.graph import StateGraph, END

from app.state import GraphState
from app.retriever import retrieve
from app.generator import generate
from app.llm import llm


def rewrite_question(state):

    question = state["question"]
    history = state.get("chat_history", [])

    if not history:
        return {
            "original_question": question,
            "question": question,
        }

    history_text = "\n".join(
        f"{m['role']}: {m['content']}"
        for m in history[-6:]
    )

    prompt = f"""
Rewrite the user's latest question into a standalone search query.

Use the conversation history to resolve references such as:
it, its, they, them, this, that, these, those, above, previous, etc.

Do not answer the question.
Return ONLY the rewritten question.

Conversation:
{history_text}

Latest question:
{question}
"""

    response = llm.invoke(prompt)

    rewritten = response.content.strip()

    return {
        "original_question": question,
        "question": rewritten,
    }


builder = StateGraph(GraphState)

builder.add_node(
    "rewrite",
    rewrite_question,
)

builder.add_node(
    "retrieve",
    retrieve,
)

builder.add_node(
    "generate",
    generate,
)

builder.set_entry_point("rewrite")

builder.add_edge(
    "rewrite",
    "retrieve",
)

builder.add_edge(
    "retrieve",
    "generate",
)

builder.add_edge(
    "generate",
    END,
)

graph = builder.compile()
