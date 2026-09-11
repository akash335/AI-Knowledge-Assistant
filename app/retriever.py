import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from app.embeddings import get_embeddings
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

    embeddings = get_embeddings()

    index_file = os.path.join(
        VECTOR_DB_PATH,
        "index.faiss"
    )

    os.makedirs(
        VECTOR_DB_PATH,
        exist_ok=True
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

    db.save_local(
        VECTOR_DB_PATH
    )

    print(
        f"✅ Indexed {filename} ({len(chunks)} chunks)"
    )


def ensure_vector_store():

    index_file = os.path.join(
        VECTOR_DB_PATH,
        "index.faiss"
    )

    if os.path.exists(index_file):
        return

    os.makedirs(
        VECTOR_DB_PATH,
        exist_ok=True
    )

    data_dir = "data"

    if not os.path.exists(data_dir):
        return

    pdfs = [
        os.path.join(data_dir, filename)
        for filename in os.listdir(data_dir)
        if filename.lower().endswith(".pdf")
    ]

    for pdf in pdfs:
        build_vector_store(pdf)


def retrieve(state):

    ensure_vector_store()

    index_file = os.path.join(
        VECTOR_DB_PATH,
        "index.faiss"
    )

    if not os.path.exists(index_file):

        return {
            "documents": []
        }

    embeddings = get_embeddings()

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