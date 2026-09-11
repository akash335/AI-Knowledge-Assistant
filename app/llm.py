from langchain_groq import ChatGroq

from app.config import GROQ_API_KEY

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    groq_api_key=GROQ_API_KEY,
)
