from langchain_ollama import ChatOllama
from pydantic import BaseModel,Field
from typing import List


llm = ChatOllama(model = "llama3.2")


# history = []

# while True:
 
#   user = input("Hey im AI: ")

#   if user.lower() in ["bye","exit","ok"]:
#        print("thanks for visiting ")
#        break 
 
#   history.append({
#         "role": "user",
#         "content": user
#     })

#   response = llm.invoke(history)

#   print("AI : ", response.content)

#   history.append({
#         "role": "assistant",
#         "content": response.content
#     })

# data = "hello my name is vedant kapil "\
#        "my email is vedantkp79@gmail.com and my age is 21"

# res = llm.invoke(f"please give me only name email and age from this data: {data}")

# print(type(res))
# print(res.content)

# class  ResponseStrecture(BaseModel):
#     name:str = Field(description="complete name")
#     age:int = Field(description="this is my age")
#     email:str = Field(description="Email address")

# structured = llm.with_structured_output(ResponseStrecture)
# res = structured.invoke(f"please give me only name email and age from this data: {data}")
# print(type(res))
# print(res.model_dump()) 


class Movies(BaseModel):
    Title:str = Field(description="Movie Title")
    Year:int = Field(description="Year of Release")

class Movies(BaseModel):
    movies: List[Movies]    

structured = llm.with_structured_output(Movies)
des = structured.invoke("give me four action movie")   
 
# print(des.content)
print(des.model_dump())