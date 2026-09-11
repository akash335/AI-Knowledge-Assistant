from langgraph.graph import StateGraph
from langgraph.graph import END

from app.state import GraphState
from app.retriever import retrieve
from app.generator import generate

builder = StateGraph(GraphState)

builder.add_node(
    "retrieve",
    retrieve
)

builder.add_node(
    "generate",
    generate
)

builder.set_entry_point("retrieve")

builder.add_edge(
    "retrieve",
    "generate"
)

builder.add_edge(
    "generate",
    END
)

graph = builder.compile()