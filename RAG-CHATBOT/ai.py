from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma

# LLM
llm = ChatOllama(
    model="llama3.2"
)

# Load PDF
loader = PyPDFLoader("Vedant_Kapil_Resume.pdf")
docs = loader.load()

# Split
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

# Chunks
chunks = splitter.split_documents(docs)

# Embeddings
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# Vector Database
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

while True:

    question = input("Ask: ")

    if question.lower() == "bye":
        print("Thank you")
        break

    results = vectorstore.similarity_search(
        question,
        k=2
    )

    for doc in results:
        print(doc.page_content)