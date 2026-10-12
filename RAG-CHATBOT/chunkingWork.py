#-------------------------------------recursive chunk example-----------------------------------------------------

# from langchain_community.document_loaders import Docx2txtLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter

# data = Docx2txtLoader("testing.docx")
# documents= data.load()

# splitter = RecursiveCharacterTextSplitter(
#     chunk_size = 7,
#     chunk_overlap=1
# )
# chunks = splitter.split_documents(documents)
# for chunk in chunks:
#     print("Chunks:",chunk.page_content)


#---------------------------------semantic chunks example---------------------------------------------------------
from llama_parse import LlamaParse
from langchain_community.document_loaders import Docx2txtLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv
load_dotenv()


data = Docx2txtLoader("testing.docx")
documents= data.load()

embedding = OllamaEmbeddings(model="nomic-embed-text:latest")

splitter = SemanticChunker(embeddings=embedding)

chunks = splitter.split_documents(documents)
for chunk in chunks:
    print(chunk)
    
