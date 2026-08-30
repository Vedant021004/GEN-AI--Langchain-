import os

from dotenv import load_dotenv
from llama_parse import LlamaParse
from langchain_core.documents import Document


# ==========================================
# 1. LOAD API KEY
# ==========================================

load_dotenv()

LLAMA_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")


# ==========================================
# 2. CREATE LLAMAPARSE PARSER
# ==========================================

parser = LlamaParse(
    api_key=LLAMA_API_KEY,
    result_type="markdown"
)


# ==========================================
# 3. PARSE PDF
# ==========================================

parsed_documents = parser.load_data(
    "Vedant_Kapil_Resume.pdf"
)


# ==========================================
# 4. CREATE LANGCHAIN DOCUMENTS
# ==========================================

docs = []

for doc in parsed_documents:

    new_document = Document(
        page_content=doc.text,

        metadata={
            "source": "Vedant_Kapil_Resume.pdf",
            "document_type": "resume",
            "owner": "Vedant Kapil"
        }
    )

    docs.append(new_document)


# ==========================================
# 5. CHECK RESULT
# ==========================================

print("Number of documents:", len(docs))


for i, doc in enumerate(docs):

    print("\n========================")
    print("DOCUMENT:", i)
    print("========================")

    print("\nTEXT:")
    print(doc.page_content)

    print("\nMETADATA:")
    print(doc.metadata)