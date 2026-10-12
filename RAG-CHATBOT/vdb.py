from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from pprint import pprint

# # Creating documents:
# creating objects of documents then storing them in a list to pass it down in chroma

doc1=Document(
    page_content="This document consists of red apple",
    metadata={"fruit":"Apple"}
)

doc2=Document(
    page_content="This documents consists of yellow mango",
    metadata={"fruit":"Mango"}
)

doc3=Document(
    page_content="This document consists of pink lychee ",
    metadata={"fruit":"Lychee"}
)

doc4=Document(
    page_content="This document consists of yellow banana",
    metadata={"fruit":"Bnanana"}
)

docs=[doc1,doc2,doc3,doc4]

# # Embeddings:
# creating embedding model and storing it into chroma db

embedding = OllamaEmbeddings(model="nomic-embed-text")

vdb=Chroma(
    embedding_function=embedding,
    persist_directory="practice_chroma_db",
    collection_name="Sampling"
)
vdb.add_documents(docs)

# # Similarity Search with and w/o Score:
# similarity search will check the similarity and then will return similar documents on the basis of "k" with and without score as per our choice
#
# score nearest to 0 = good similarity 
# otheriwse = no

#Similarity search
response= vdb.similarity_search(
            query="which among this is red in color",
            k=1
        )
for ans in response:
    print("\nRESPONSE: ",ans.page_content)
    
print()
print()


result=vdb.get(include=['embeddings','documents','metadatas'])
print("\nORIGINAL DOCS: \n")
pprint(result)

#similarity search with score
response=vdb.similarity_search_with_score(
    query="Which among these documents have yellow banana?",
    k=1
)
print("\nRESPONSE:",response)

# # Updating existing documents:
# it can update the existing document through file id by using a predefined function of .update_document

UpdatedDoc= Document(
    page_content="This is green grapes",
    metadata={"fruit":"Grapes"}
)
vdb.update_document(document_id="56a75eab-7a76-4372-a799-1b8576f976ba",document=UpdatedDoc)
result=vdb.get(include=['documents','metadatas'])
print("\nUPDATED DOC:\n")
pprint(result)

# #  Deleting existing documents:
# need file id to delete any exisiting document

vdb.delete(ids="56a75eab-7a76-4372-a799-1b8576f976ba")
result=vdb.get(include=['documents','metadatas'])
print("\nDELETED DOC:\n")
pprint(result)
