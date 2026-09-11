import os
import requests
import streamlit as st


API_URL = os.getenv(
    "API_URL",
    "https://ai-knowledge-assistant-ewuq.onrender.com"
)


st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>

    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 6rem;
    }

    div[data-testid="stSidebar"] {
        min-width: 280px;
        max-width: 280px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


st.title("🤖 AI Knowledge Assistant")
st.caption("Powered by LangGraph • FAISS • Groq")


if "messages" not in st.session_state:
    st.session_state.messages = []


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("📚 Knowledge Base")

    os.makedirs(
        "data",
        exist_ok=True,
    )

    pdfs = sorted(
        [
            f
            for f in os.listdir("data")
            if f.lower().endswith(".pdf")
        ]
    )

    st.success(
        f"{len(pdfs)} PDF(s) Indexed"
    )

    with st.expander(
        "📄 Indexed Documents",
        expanded=False,
    ):

        if pdfs:

            for pdf in pdfs:
                st.write(f"• {pdf}")

        else:
            st.info("No PDFs indexed.")

    st.divider()

    st.subheader("Upload PDF")

    uploaded = st.file_uploader(
        "Choose a PDF",
        type=["pdf"],
        help="Maximum 200 MB",
    )

    if uploaded:

        if st.button(
            "⬆️ Upload & Index",
            use_container_width=True,
        ):

            files = {
                "file": (
                    uploaded.name,
                    uploaded.getvalue(),
                    "application/pdf",
                )
            }

            with st.spinner(
                "Indexing document..."
            ):

                try:

                    response = requests.post(
                        f"{API_URL}/upload",
                        files=files,
                        timeout=180,
                    )

                    if response.status_code == 200:

                        data = response.json()

                        if data["status"] == "exists":

                            st.warning(
                                "This PDF is already indexed."
                            )

                        else:

                            st.success(
                                "PDF indexed successfully."
                            )

                        st.rerun()

                    else:

                        st.error(
                            response.text
                        )

                except Exception as e:

                    st.error(
                        f"Upload error: {e}"
                    )

    st.divider()

    if st.button(
        "🗑 Clear Chat",
        use_container_width=True,
    ):

        st.session_state.messages = []

        st.rerun()


# ==========================================================
# WELCOME
# ==========================================================

if not st.session_state.messages:

    st.markdown(
        """
        ## 👋 Welcome!

        Ask questions about your uploaded documents.

        **Try:**

        - What is gradient boosting?
        - What are its advantages?
        - Explain AWS Lambda.
        - Summarize the machine learning document.
        """
    )


# ==========================================================
# HISTORY
# ==========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        if message.get("sources"):

            with st.expander(
                "📚 Sources"
            ):

                for source in message["sources"]:

                    st.write(
                        f"📄 {source}"
                    )


# ==========================================================
# INPUT
# ==========================================================

prompt = st.chat_input(
    "Ask anything about your documents..."
)


if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Send only previous conversation turns.
    # Current question is sent separately.
    history = [
        {
            "role": m["role"],
            "content": m["content"],
        }
        for m in st.session_state.messages[:-1]
    ]

    with st.chat_message("assistant"):

        placeholder = st.empty()

        with st.spinner("Thinking..."):

            try:

                response = requests.post(
                    f"{API_URL}/chat",
                    json={
                        "question": prompt,
                        "chat_history": history,
                    },
                    timeout=180,
                )

                response.raise_for_status()

                data = response.json()

                answer = data.get(
                    "answer",
                    "I couldn't find that information.",
                )

                placeholder.markdown(
                    answer
                )

                sources = []
                seen = set()

                for source in data.get(
                    "sources",
                    [],
                ):

                    filename = source.get(
                        "file",
                        "Unknown",
                    )

                    page = source.get(
                        "page"
                    )

                    if page is not None:

                        display = (
                            f"{filename} | "
                            f"Page {page + 1}"
                        )

                    else:

                        display = filename

                    if display not in seen:

                        seen.add(display)

                        sources.append(
                            display
                        )

                if sources:

                    st.divider()

                    with st.expander(
                        "📚 Sources"
                    ):

                        for source in sources:

                            st.write(
                                f"📄 {source}"
                            )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                })

            except requests.exceptions.ConnectionError:

                placeholder.error(
                    "❌ API server is not running."
                )

            except requests.exceptions.Timeout:

                placeholder.error(
                    "⏱️ Request timed out."
                )

            except Exception as e:

                placeholder.error(
                    f"❌ Error: {e}"
                )
