from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="nomic-embed-text")

vector = embeddings.embed_query("Hello I am Pizza.. Are you burger??")

print("type: ",type(vector))
print("Length: ",len(vector))
print("embedding: ", vector)
