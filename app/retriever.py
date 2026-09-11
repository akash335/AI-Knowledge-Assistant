from langchain_community.vectorstores import FAISS

from app.embeddings import embeddings
from app.config import VECTOR_DB_PATH

vectorstore = FAISS.load_local(
    VECTOR_DB_PATH,
    embeddings,
    allow_dangerous_deserialization=True,
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 4}
)

def retrieve(state):

    docs = retriever.invoke(state["question"])

    return {
        "documents": docs
    }