import tempfile
import streamlit as st

from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver


st.set_page_config(page_title="Agentic PDF Chatbot")
st.title("📄 Agentic PDF Chatbot")


# ------------------------------------
# Global Variables
# ------------------------------------

vector_db = None
agent = None


# ------------------------------------
# Models
# ------------------------------------

llm = ChatOllama(
    model="qwen3:latest"
)

embedding = OllamaEmbeddings(
    model="nomic-embed-text"
)


# ------------------------------------
# Tool
# ------------------------------------

@tool
def retrieve_context(question: str) -> str:
    """
    Retrieve relevant information from the uploaded PDF.
    """

    global vector_db

    print("Tool Called")

    if vector_db is None:
        return "No PDF has been uploaded."

    docs = vector_db.similarity_search(
        query=question,
        k=3
    )

    if len(docs) == 0:
        return "No relevant information found."

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    print(context)

    return context


# ------------------------------------
# Upload PDF
# ------------------------------------

uploaded_file = st.file_uploader(
    "Upload PDF",
    type="pdf"
)

if uploaded_file is not None:

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp:

        temp.write(uploaded_file.read())

        pdf_path = temp.name

    loader = PyPDFLoader(pdf_path)

    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(docs)

    vector_db = InMemoryVectorStore.from_documents(
        documents=chunks,
        embedding=embedding
    )

    memory = InMemorySaver()

    agent = create_agent(
        model=llm,
        tools=[retrieve_context],
        system_prompt="""
You are a PDF Assistant.

You MUST call retrieve_context before answering any question.

Never answer from your own knowledge.

Use ONLY the retrieved context.

If the answer is not present,
reply:

'I couldn't find that information in the uploaded PDF.'
""",
        checkpointer=memory
    )

    st.success("✅ PDF Uploaded Successfully")

    st.session_state.agent = agent


# ------------------------------------
# Chat
# ------------------------------------

if "agent" in st.session_state:

    question = st.chat_input("Ask anything...")

    if question:

        with st.chat_message("user"):
            st.write(question)

        response = st.session_state.agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            },
            config={
                "configurable": {
                    "thread_id": "1"
                }
            }
        )

        answer = response["messages"][-1].content

        with st.chat_message("assistant"):
            st.write(answer)