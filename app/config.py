"""
Project configuration.

Loads environment variables from the .env file.
"""

import os

from dotenv import load_dotenv

load_dotenv()

# Groq API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Embedding Model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Vector DB Folder
VECTOR_DB_PATH = "vectorstore"

# PDF Folder
DATA_PATH = "data"