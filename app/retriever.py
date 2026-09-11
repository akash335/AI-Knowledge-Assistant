import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from app.embeddings import embeddings
from app.config import VECTOR_DB_PATH


def build_vector_store(pdf_path):

    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    filename = os.path.basename(pdf_path)

    for doc in docs:
        doc.metadata["filename"] = filename

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(docs)

    index_file = os.path.join(
        VECTOR_DB_PATH,
        "index.faiss"
    )

    if os.path.exists(index_file):

        db = FAISS.load_local(
            VECTOR_DB_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

        db.add_documents(chunks)

    else:

        db = FAISS.from_documents(
            chunks,
            embeddings
        )

    db.save_local(VECTOR_DB_PATH)

    print(
        f"✅ Indexed {filename} ({len(chunks)} chunks)"
    )


def retrieve(state):

    vectorstore = FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 8,
            "fetch_k": 20,
            "lambda_mult": 0.7
        }
    )

    docs = retriever.invoke(
        state["question"]
    )

    return {
        "documents": docs
    }
