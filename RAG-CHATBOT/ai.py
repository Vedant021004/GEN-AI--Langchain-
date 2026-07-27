from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings,ChatOllama
from langchain_chroma import Chroma

llm = ChatOllama(
    model = "llama3.2"
)


# DATA LOADING

Loader = PyPDFLoader("Vedant_Kapil_Resume.pdf")
docs = Loader.load()

# SPILITING THE TEXT

split = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
chunks = split.split_documents(docs)

# VECTOR EMBEDDING

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# STORE THE DATA INTO VECTOR DATABSE

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)


while True:

    question = llm.invoke("Ask: ")

        if question.lower() in ["bye"]:
        print("thank you")
        break

result = vectorstore.similarity_search(query = question,k=2)

print(result.page_content)