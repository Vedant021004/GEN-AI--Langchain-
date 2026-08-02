import streamlit as st
import tempfile, os

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.agents import create_agent
from langchain.tools import tool
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


# -------------------------------
# Tool
# -------------------------------
@tool
def retrieve_context(question: str) -> str:
    vector_db = st.session_state.get("vector_db")
    if vector_db is None:
        return "⚠️ No PDF uploaded yet."

    docs = vector_db.similarity_search(question, k=5)
    if not docs:
        return f"❌ No match found in the PDF for: {question}"

    return "\n\n".join(doc.page_content for doc in docs)



# -------------------------------
# Agent Creation
# -------------------------------
def create_pdf_agent():
    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        api_key=st.secrets["GROQ_API_KEY"]
    )
    memory = InMemorySaver()

    return create_agent(
        model=llm,
        tools=[retrieve_context],
        system_prompt="""
You are a PDF Assistant.
Always use the retrieve_context tool to answer questions about the uploaded PDF.
Never answer from your own knowledge.
Only use information returned by retrieve_context.
If the retrieved context does not contain the answer, reply exactly:
"I couldn't find that information in the uploaded PDF."
""",
        checkpointer=memory
    )


# -------------------------------
# PDF Processing
# -------------------------------
def process_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        temp.write(uploaded_file.read())
        pdf_path = temp.name

    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    vector_db = Chroma.from_documents(documents=chunks, embedding=embedding)

    os.remove(pdf_path)  # cleanup temp file
    return vector_db


# -------------------------------
# Upload PDF
# -------------------------------
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file is not None and st.session_state["agent"] is None:
    # Reset old PDF data
    st.session_state["vector_db"] = None
    st.session_state["agent"] = None
    st.session_state["chat_history"] = []

    # Process new PDF
    st.session_state["vector_db"] = process_pdf(uploaded_file)
    st.session_state["agent"] = create_pdf_agent()

    st.success("✅ PDF Uploaded Successfully")


# -------------------------------
# Chat Interface
# -------------------------------
if st.session_state.get("agent") is not None:

    # Display previous chat history
    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # New question
    question = st.chat_input("Ask anything...")
    if question:
        st.session_state["chat_history"].append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        try:
            response = st.session_state["agent"].invoke(
                {"messages": [{"role": "user", "content": question}]},
                config={"configurable": {"thread_id": "1"}}
            )
            answer = response["messages"][-1].content
        except Exception as e:
            answer = f"⚠️ Error: {str(e)}"

        st.session_state["chat_history"].append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.write(answer)

# -------------------------------
# Clear Chat
# -------------------------------
if st.button("🗑️ Clear Chat"):
    st.session_state["chat_history"] = []
    st.success("Chat cleared.")
