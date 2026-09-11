import os
import requests
import streamlit as st


# ==========================================================
# CONFIG
# ==========================================================

API_URL = os.getenv(
    "API_URL",
    "https://ai-knowledge-assistant-ewuq.onrender.com"
).rstrip("/")


st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================================
# CUSTOM CSS
# ==========================================================

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


# ==========================================================
# TITLE
# ==========================================================

st.title("🤖 AI Knowledge Assistant")
st.caption("Powered by LangGraph • FAISS • Groq")


# ==========================================================
# SESSION STATE
# ==========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("📚 Knowledge Base")

    # ------------------------------------------------------
    # Get documents from backend
    # ------------------------------------------------------

    try:

        response = requests.get(
            f"{API_URL}/documents",
            timeout=30,
        )

        if response.status_code == 200:

            document_data = response.json()

            pdfs = sorted(
                document_data.get(
                    "documents",
                    []
                )
            )

        else:

            pdfs = []

    except Exception:

        # Fallback to PDFs bundled with Streamlit app
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


    # ------------------------------------------------------
    # PDF count
    # ------------------------------------------------------

    st.success(
        f"{len(pdfs)} PDF(s) Indexed"
    )


    # ------------------------------------------------------
    # Indexed documents
    # ------------------------------------------------------

    with st.expander(
        "📄 Indexed Documents",
        expanded=False,
    ):

        if pdfs:

            for pdf in pdfs:

                st.write(
                    f"• {pdf}"
                )

        else:

            st.info(
                "No PDFs indexed."
            )


    st.divider()


    # ======================================================
    # UPLOAD PDF
    # ======================================================

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
                "Uploading and indexing document..."
            ):

                try:

                    # IMPORTANT:
                    # Upload goes to /upload,
                    # NOT /chat.

                    response = requests.post(
                        f"{API_URL}/upload",
                        files=files,
                        timeout=300,
                    )


                    # --------------------------------------------------
                    # Successful upload
                    # --------------------------------------------------

                    if response.status_code == 200:

                        data = response.json()

                        status = data.get(
                            "status",
                            ""
                        )

                        filename = data.get(
                            "filename",
                            uploaded.name,
                        )


                        if status == "exists":

                            st.warning(
                                f"📄 {filename} is already indexed."
                            )

                        elif status == "success":

                            st.success(
                                f"✅ {filename} uploaded and indexed successfully."
                            )

                        else:

                            st.success(
                                "✅ PDF uploaded successfully."
                            )


                        # Refresh sidebar document list
                        st.rerun()


                    # --------------------------------------------------
                    # Backend error
                    # --------------------------------------------------

                    else:

                        try:

                            error_data = response.json()

                            error_message = error_data.get(
                                "detail",
                                response.text,
                            )

                        except Exception:

                            error_message = response.text


                        st.error(
                            f"Upload error: {error_message}"
                        )


                except requests.exceptions.Timeout:

                    st.error(
                        "⏱️ Upload timed out. "
                        "The PDF may be large or indexing is still taking too long."
                    )


                except requests.exceptions.ConnectionError:

                    st.error(
                        "❌ Could not connect to the backend."
                    )


                except Exception as e:

                    st.error(
                        f"❌ Upload error: {e}"
                    )


    st.divider()


    # ======================================================
    # CLEAR CHAT
    # ======================================================

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
# CHAT HISTORY
# ==========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


        # --------------------------------------------------
        # Sources
        # --------------------------------------------------

        if message.get("sources"):

            with st.expander(
                "📚 Sources"
            ):

                for source in message["sources"]:

                    st.write(
                        f"📄 {source}"
                    )


# ==========================================================
# CHAT INPUT
# ==========================================================

prompt = st.chat_input(
    "Ask anything about your documents..."
)


# ==========================================================
# CHAT REQUEST
# ==========================================================

if prompt:

    # ------------------------------------------------------
    # Add current user message
    # ------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )


    with st.chat_message(
        "user"
    ):

        st.markdown(
            prompt
        )


    # ------------------------------------------------------
    # Send ONLY previous conversation turns
    # ------------------------------------------------------

    history = [
        {
            "role": m["role"],
            "content": m["content"],
        }
        for m in st.session_state.messages[:-1]
    ]


    # ------------------------------------------------------
    # Assistant response
    # ------------------------------------------------------

    with st.chat_message(
        "assistant"
    ):

        placeholder = st.empty()


        with st.spinner(
            "Thinking..."
        ):

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


                # --------------------------------------------------
                # Answer
                # --------------------------------------------------

                answer = data.get(
                    "answer",
                    "I couldn't find that information.",
                )


                placeholder.markdown(
                    answer
                )


                # --------------------------------------------------
                # Sources
                # --------------------------------------------------

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

                        seen.add(
                            display
                        )

                        sources.append(
                            display
                        )


                # --------------------------------------------------
                # Display sources
                # --------------------------------------------------

                if sources:

                    st.divider()


                    with st.expander(
                        "📚 Sources"
                    ):

                        for source in sources:

                            st.write(
                                f"📄 {source}"
                            )


                # --------------------------------------------------
                # Save assistant message
                # --------------------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                    }
                )


            # --------------------------------------------------
            # Connection error
            # --------------------------------------------------

            except requests.exceptions.ConnectionError:

                placeholder.error(
                    "❌ API server is not reachable."
                )


            # --------------------------------------------------
            # Timeout
            # --------------------------------------------------

            except requests.exceptions.Timeout:

                placeholder.error(
                    "⏱️ Request timed out."
                )


            # --------------------------------------------------
            # Other error
            # --------------------------------------------------

            except Exception as e:

                placeholder.error(
                    f"❌ Error: {e}"
                )