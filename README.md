# 🤖 AI Knowledge Assistant

A Retrieval-Augmented Generation (RAG) application that allows users to ask questions about their PDF documents and receive context-aware answers with source and page references.

## 🚀 Live Demo

**Frontend:**  
https://ai-knowledge-assistant23.streamlit.app/

**Backend API:**  
https://ai-knowledge-assistant-ewuq.onrender.com

---

## ✨ Features

- 📄 Multiple PDF document support
- ⬆️ PDF upload and automatic indexing
- 🔍 Semantic search using FAISS
- 🧠 FastEmbed embeddings
- 🔄 LangGraph-based RAG workflow
- 🤖 Groq-powered LLM responses
- 💬 Conversation follow-up questions
- 📝 Chat history
- 📚 Source and page references
- 🛡️ Duplicate upload protection
- ⚡ FastAPI backend
- 🎨 Streamlit frontend

---

## 🏗️ Architecture

```text
                PDF Documents
                      │
                      ▼
               PyPDFLoader
                      │
                      ▼
                Text Chunking
                      │
                      ▼
              FastEmbed Embeddings
                      │
                      ▼
                   FAISS
                      │
                      ▼
              Semantic Retrieval
                      │
                      ▼
                LangGraph
                      │
                      ▼
                  Groq LLM
                      │
                      ▼
              Answer + Sources
                      │
                      ▼
                Streamlit UI

🔄 RAG Workflow

The application follows a multi-step RAG pipeline:

Question Input
The user submits a question through the Streamlit interface.
Question Rewriting
LangGraph uses conversation history to rewrite follow-up questions into standalone search queries.
Document Retrieval
FAISS performs semantic similarity search over indexed document chunks.
Context Generation
The retrieved document chunks are passed to the generation step.
LLM Response
Groq generates an answer based on the retrieved context.
Source Attribution
Relevant PDF filenames and page references are returned with the answer.
🛠️ Tech Stack
Technology	Purpose
Python	Core programming language
FastAPI	Backend REST API
Streamlit	Frontend UI
LangGraph	RAG workflow orchestration
LangChain	LLM and document-processing framework
FAISS	Vector similarity search
FastEmbed	Document embeddings
Groq	Large Language Model inference
PyPDFLoader	PDF document loading
Render	Backend deployment
Streamlit Cloud	Frontend deployment
📁 Project Structure
AI-Knowledge-Assistant/
│
├── app/
│   ├── api.py
│   ├── config.py
│   ├── embeddings.py
│   ├── generator.py
│   ├── graph.py
│   ├── llm.py
│   ├── retriever.py
│   └── state.py
│
├── frontend/
│   └── app.py
│
├── data/
│   └── *.pdf
│
├── tests/
│
├── chat.py
├── index.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env
⚙️ Local Setup
1. Clone the repository
git clone https://github.com/akash335/AI-Knowledge-Assistant.git
cd AI-Knowledge-Assistant
2. Create a virtual environment
python -m venv venv
source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Configure environment variables

Create a .env file:

GROQ_API_KEY=your_groq_api_key
▶️ Run Backend
uvicorn app.api:app --reload --port 8000

Backend will be available at:

http://127.0.0.1:8000
🎨 Run Frontend

In another terminal:

streamlit run frontend/app.py

The Streamlit application will open in your browser.

📚 Example Questions

Try asking:

What is AWS?
What is gradient boosting?
What are the advantages of gradient boosting?
Explain AWS Lambda.
Summarize the machine learning document.

You can also ask follow-up questions using the previous conversation context.

🔐 Environment Variables

The application requires:

GROQ_API_KEY=your_groq_api_key

For deployment, configure the environment variable through the hosting platform rather than committing .env to the repository.

☁️ Deployment
Backend

The FastAPI backend is deployed on Render.

Frontend

The Streamlit frontend is deployed on Streamlit Community Cloud.

The frontend communicates with the deployed FastAPI backend through its REST API.

📌 Key Concepts Demonstrated

This project demonstrates practical implementation of:

Retrieval-Augmented Generation (RAG)
Vector databases
Semantic search
Document chunking
Embedding models
LangGraph workflows
LLM integration
Conversational question rewriting
Source attribution
REST API development
Cloud deployment
👨‍💻 Author

Akash Porumamilla