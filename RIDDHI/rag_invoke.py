from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma

# -------------------------
# LLM
# -------------------------

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)

# -------------------------
# Load PDF
# -------------------------

loader = PyPDFLoader("Vedant_Kapil_Resume.pdf")
docs = loader.load()

# -------------------------
# Chunking
# -------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(docs)

print("Number of chunks:", len(chunks))

# -------------------------
# Embeddings
# -------------------------

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# -------------------------
# ChromaDB
# -------------------------

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./vedant_db"
)

# -------------------------
# RAG LOOP
# -------------------------

while True:

    question = input("\nAsk: ")

    if question.lower() == "bye":
        print("Thank you!")
        break

    # Retrieve top 3 chunks
    results = vectorstore.similarity_search(
        question,
        k=3
    )

    # Create context
    context = "\n\n".join(
        doc.page_content
        for doc in results
    )

    # Prompt
    prompt = f"""
You are an assistant that answers questions about Vedant Kapil.

Use ONLY the information in the resume context.

Resume context:
{context}

Question:
{question}

Rules:
- Answer naturally.
- Do not invent information.
- Do not use outside knowledge.
- If the answer is not present in the resume, say:
  "I could not find that information in Vedant's resume."
"""

    # Generate answer
    response = llm.invoke(prompt)

    print("\nAnswer:")
    print(response.content)