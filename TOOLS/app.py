import streamlit as st
import tempfile, os

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver


# -------------------------------
# Streamlit Config
# -------------------------------
st.set_page_config(page_title="Agentic PDF Chatbot")
st.title("📄 Agentic PDF Chatbot")

# -------------------------------
# Session State Initialization
# -------------------------------
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "vector_db" not in st.session_state:
    st.session_state["vector_db"] = None
if "agent" not in st.session_state:
    st.session_state["agent"] = None
if "raw_chunks" not in st.session_state:
    # Keeps plain text of every chunk for keyword fallback search
    st.session_state["raw_chunks"] = []
if "last_retrieval_debug" not in st.session_state:
    st.session_state["last_retrieval_debug"] = ""


# -------------------------------
# Hybrid Retrieval Tool
# (keyword match + semantic search, deduped)
# -------------------------------
@tool
def retrieve_context(question: str) -> str:
    """Retrieve relevant information from the uploaded PDF.
    Combines exact keyword matching (good for names, numbers, IDs)
    with semantic vector search (good for conceptual questions).
    Always call this tool before answering any question about the PDF.
    """
    vector_db = st.session_state.get("vector_db")
    raw_chunks = st.session_state.get("raw_chunks", [])

    if vector_db is None:
        return "No PDF has been uploaded."

    results = []

    # --- 1. Keyword fallback: catches exact names/terms embeddings may miss ---
    q_lower = question.lower().strip()
    # Only do keyword matching on meaningful words (skip very short/common words)
    keywords = [w for w in q_lower.split() if len(w) > 2]

    for chunk in raw_chunks:
        chunk_lower = chunk.lower()
        if q_lower in chunk_lower or any(kw in chunk_lower for kw in keywords):
            results.append(chunk)

    # --- 2. Semantic search ---
    try:
        semantic_docs = vector_db.similarity_search(question, k=5)
        for doc in semantic_docs:
            results.append(doc.page_content)
    except Exception as e:
        results.append(f"[Semantic search error: {e}]")

    # --- Dedupe while preserving order ---
    seen = set()
    deduped = []
    for r in results:
        if r not in seen:
            seen.add(r)
            deduped.append(r)

    # Save for debug panel
    st.session_state["last_retrieval_debug"] = "\n\n---\n\n".join(deduped[:8]) if deduped else "(nothing retrieved)"

    if not deduped:
        return "No relevant information found."

    # Cap how much context we send to the LLM
    return "\n\n".join(deduped[:8])


# -------------------------------
# Agent Creation
# -------------------------------
def create_pdf_agent():
    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        api_key=st.secrets["GROQ_API_KEY"],
        temperature=0,
    )
    memory = InMemorySaver()

    return create_agent(
        model=llm,
        tools=[retrieve_context],
        system_prompt="""You are a PDF Assistant.

You MUST call the retrieve_context tool for every question about the
uploaded PDF before answering — never skip this step, even if you think
you already know the answer.

Only use information returned by retrieve_context to answer.
If the retrieved context does not contain the answer, reply exactly:
"I couldn't find that information in the uploaded PDF."
""",
        checkpointer=memory,
    )


# -------------------------------
# PDF Processing
# -------------------------------
def process_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        temp.write(uploaded_file.read())
        pdf_path = temp.name

    try:
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()

        # Larger chunks + overlap so names/context aren't split across boundaries
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)

        embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

        # Fresh, isolated in-memory collection per upload (avoids stale data across sessions)
        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=embedding,
            collection_name=f"pdf_{next(tempfile._get_candidate_names())}",
        )

        raw_chunks = [c.page_content for c in chunks]
    finally:
        os.remove(pdf_path)

    return vector_db, raw_chunks


# -------------------------------
# Sidebar: Debug Panel
# -------------------------------
with st.sidebar:
    st.header("🔍 Debug")
    show_debug = st.checkbox("Show retrieved context", value=False)
    if st.session_state["vector_db"] is not None:
        st.caption(f"Chunks indexed: {len(st.session_state['raw_chunks'])}")


# -------------------------------
# Upload PDF
# -------------------------------
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file is not None and st.session_state["agent"] is None:
    st.session_state["vector_db"] = None
    st.session_state["agent"] = None
    st.session_state["chat_history"] = []
    st.session_state["raw_chunks"] = []

    with st.spinner("Processing PDF..."):
        vector_db, raw_chunks = process_pdf(uploaded_file)
        st.session_state["vector_db"] = vector_db
        st.session_state["raw_chunks"] = raw_chunks
        st.session_state["agent"] = create_pdf_agent()

    st.success(f"✅ PDF Uploaded Successfully ({len(raw_chunks)} chunks indexed)")


# -------------------------------
# Chat Interface
# -------------------------------
if st.session_state.get("agent") is not None:

    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    question = st.chat_input("Ask anything...")
    if question:
        st.session_state["chat_history"].append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        try:
            response = st.session_state["agent"].invoke(
                {"messages": [{"role": "user", "content": question}]},
                config={"configurable": {"thread_id": "1"}},
            )
            answer = response["messages"][-1].content
        except Exception as e:
            answer = f"⚠️ Error: {str(e)}"

        st.session_state["chat_history"].append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.write(answer)
            if show_debug:
                with st.expander("Retrieved context (debug)"):
                    st.text(st.session_state.get("last_retrieval_debug", "(none)"))

# -------------------------------
# Clear Chat
# -------------------------------
if st.button("🗑️ Clear Chat"):
    st.session_state["chat_history"] = []
    st.success("Chat cleared.")