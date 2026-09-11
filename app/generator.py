from app.llm import llm


def generate(state):

    docs = state["documents"]
    history = state.get("chat_history", [])

    if not docs:
        return {
            "answer": "I couldn't find that information.",
            "sources": []
        }

    context = "\n\n".join(
        f"File: {d.metadata.get('filename', 'Unknown')}\n"
        f"Page: {d.metadata.get('page', 0) + 1}\n"
        f"Content:\n{d.page_content}"
        for d in docs
    )

    history_text = "\n".join(
        f"{m['role']}: {m['content']}"
        for m in history[-6:]
    )

    prompt = f"""
You are an AI Knowledge Assistant.

Answer ONLY using the provided document context.

Conversation history:
{history_text}

Document context:
{context}

Current question:
{state["question"]}

Rules:
- Use conversation history to understand follow-up questions.
- Use only information supported by the documents.
- Never invent information.
- If the documents do not contain the answer, say:
  "I couldn't find that information."
- Be concise and clear.
"""

    response = llm.invoke(prompt)

    sources = []
    seen = set()

    for d in docs:

        filename = d.metadata.get(
            "filename",
            d.metadata.get("source", "Unknown")
        )

        page = d.metadata.get("page")

        key = (filename, page)

        if key not in seen:
            seen.add(key)

            sources.append({
                "file": filename,
                "page": page
            })

    return {
        "answer": response.content.strip(),
        "sources": sources
    }
