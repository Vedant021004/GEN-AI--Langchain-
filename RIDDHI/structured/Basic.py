from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv() 

## Schema

class Schema(BaseModel):
    name : str = Field(
        description="name of the author",
        min_length= 1,
        max_length= 9
    )

    age : int = Field(
        description="age of the husband"
    )


llm = ChatGroq(
    model="openai/gpt-oss-20b"
)

structure = llm.with_structured_output(Schema)


user  = input("Please Enter the value : ")
result = structure.invoke(user)


print(result.name)
print(result.age)

print("direct", result)