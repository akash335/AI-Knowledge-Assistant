import os
import shutil

DATA_DIR = "data"
VECTOR_DIR = "vectorstore"


def list_documents():
    return sorted(
        [
            f for f in os.listdir(DATA_DIR)
            if f.endswith(".pdf")
        ]
    )


def delete_document(filename):

    path = os.path.join(DATA_DIR, filename)

    if os.path.exists(path):
        os.remove(path)


def rebuild_vector_store():

    from app.retriever import build_vector_store

    if os.path.exists(VECTOR_DIR):
        shutil.rmtree(VECTOR_DIR)

    os.makedirs(VECTOR_DIR, exist_ok=True)

    for pdf in list_documents():
        build_vector_store(
            os.path.join(DATA_DIR, pdf)
        )