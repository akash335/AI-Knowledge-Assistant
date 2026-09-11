# AI Knowledge Assistant

A Retrieval-Augmented Generation (RAG) application for asking questions about PDF documents.

## Features

- Multiple PDF support
- PDF upload
- FAISS semantic search
- Sentence Transformers embeddings
- LangGraph workflow
- Groq LLM
- Streaming responses
- Conversation follow-ups
- Source and page references
- Document deletion
- Duplicate upload protection
- Chat history
- FastAPI backend
- Streamlit frontend

## Architecture

PDF
↓
PyPDFLoader
↓
Text Chunking
↓
Embeddings
↓
FAISS
↓
Retriever
↓
LangGraph
↓
Groq
↓
Answer + Sources
↓
Streamlit

## Run Backend

uvicorn app.api:app --reload --port 8000

## Run Frontend

streamlit run frontend/app.py
