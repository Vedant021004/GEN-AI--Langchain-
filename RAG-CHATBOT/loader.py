from langchain_community.document_loaders import TextLoader, WebBaseLoader

# # Text Loader

loader = TextLoader(r"Sample.txt",encoding="utf-8") # MAKE SURE U HAVE Sample.txt FILE IN YOUR FOLDER OR REPO

data = loader.load()
print("\nLOAD:\n",data)

data1 = loader.lazy_load()
for doc in data1:
    print("\nLAZY LOAD:\n",doc.page_content)

# type of data
print("\nLOAD",type(data))
print("\nLAZY LOAD",type(data1))

#length 
print("\nLENGTH OF LOAD",len(data))

# # WebBase Loader

loader = WebBaseLoader(web_path="https://www.sap.com/india/products/financial-management.html?url_id=banner-in-homepage-row4-pos1-financial-management-260512")

data=loader.load()
print(data[0].page_content)
