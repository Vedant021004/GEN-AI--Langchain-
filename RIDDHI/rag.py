from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma


# llm defined
llm = ChatOllama(
    model = "llama3.2"
)

# data defined
data = PyPDFLoader("Vedant_Kapil_Resume.pdf")
docs = data.load()

# splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50
)

# splitter ko store krna hai chunks ke andr
chunks = splitter.split_documents(docs) 
 # aur hum doc ko split krenge 

# embeddings
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# chroma from document
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./vedant_db"
)


print(chunks)