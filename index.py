import os
from app.retriever import build_vector_store

DATA_DIR = "data"

for file in os.listdir(DATA_DIR):
    if file.endswith(".pdf"):
        print(f"Indexing {file}...")
        build_vector_store(os.path.join(DATA_DIR, file))