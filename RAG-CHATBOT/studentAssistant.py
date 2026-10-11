from langchain_community.document_loaders import PyPDFLoader , UnstructuredPowerPointLoader
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import create_agent
import os
from dotenv import load_dotenv
load_dotenv()


class Assistant:
    def __init__(self,name,ai):
        self.ai = ai
        self.name = name
    def assistant(self):
        llm = ChatGroq(model="openai/gpt-oss-20b")
        memory = MemorySaver()
        agent = create_agent(
            model=llm,
            checkpointer=memory
        )
        choose = input("What do u want to upload?\n1.PDF\n2.PPt:\n")
        if(choose=="1"):
            ip = input("Enter your file path: ")
            data = PyPDFLoader(ip)
            doc = data.load()
        elif(choose=="2"):
            ip = input("Enter your file path: ")
            data = UnstructuredPowerPointLoader(ip)
            doc = data.load()

        else:
            print("INVALID OPTION")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
        # chunks= splitter.split_documents(doc)
        chunks = splitter.split_documents(doc)

        # print("Documents:", len(doc))
        # print("Chunks:", len(chunks))
        # print("First chunk:", chunks[0].page_content[:200])

        embedding = OllamaEmbeddings(model="nomic-embed-text:latest")

        vdb = Chroma.from_documents(
            documents= chunks,
            embedding= embedding,
            persist_directory="./sa_db"

        )

        while True:
            query = input(f"{self.name}: ")
            if query in ["exit","terminate"]:
                print("Terminating Conversation.. THANK YOU..")
                break

            result = vdb.similarity_search(
                query= query,
                k=5
            )
            context = "\n\n".join(
                doc.page_content
                for doc in result
                )
            
            prompt = f"""
            You are {self.ai}, a helpful student assistant.

            You answer questions about the uploaded document.

            Use the document context below when it is relevant.

            Document context:

            {context}

            Current question:

            {query}

            Rules:
            1. If the answer is available in the document context, answer using the document.
            2. If the exact answer is NOT available in the document, but the question
            is related to the same topic, you may answer using your general knowledge.
            3. If the question is completely unrelated to the document/topic, say:

            "I could not find this information."

            Give simple and clear answers suitable for a student.
            """

            response = agent.invoke({
                    "messages":[{"role":"user", "content": prompt}]
                },config={"configurable":{"thread_id":"1"}})
            
            print(f"\n{self.ai}:")
            print(response['messages'][-1].content)
            print()


name=input("Enter your name: ")
ai = input("Enter name for your class assistant: ")


a1 = Assistant(name,ai)
a1.assistant()
