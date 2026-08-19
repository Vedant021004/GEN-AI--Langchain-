from pydantic import BaseModel,Field
from typing import List
from genai_shared.chat import chat_loop, history_responder
from genai_shared.llms import ollama_llm

llm = ollama_llm()
chat_loop(
    history_responder(llm),
    prompt="Hey im AI: ",
    exit_words=frozenset({"bye", "exit", "ok"}),
    farewell="thanks for visiting ",
    answer_prefix="AI : ",
)

data = "hello my name is vedant kapil "\
       "my email is vedantkp79@gmail.com and my age is 21"

res = llm.invoke(f"please give me only name email and age from this data: {data}")

print(type(res))
print(res.content)

class  ResponseStrecture(BaseModel):
    name:str = Field(description="complete name")
    age:int = Field(description="this is my age")
    email:str = Field(description="Email address")

structured = llm.with_structured_output(ResponseStrecture)
res = structured.invoke(f"please give me only name email and age from this data: {data}")
print(type(res))
print(res.model_dump()) 


class Movies(BaseModel):
    Title:str = Field(description="Movie Title")
    Year:int = Field(description="Year of Release")

class Movies(BaseModel):
    movies: List[Movies]    

structured = llm.with_structured_output(Movies)
des = structured.invoke("give me four action movie")   
 
# print(des.content)
print(des.model_dump())