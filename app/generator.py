from app.llm import llm

def generate(state):

    docs = state["documents"]

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    prompt = f"""
You are an AI assistant.

Answer ONLY from the context.

If you don't know, say:

"I couldn't find that in the uploaded documents."

Context:

{context}

Question:

{state["question"]}

Answer:
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content
    }