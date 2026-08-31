from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


class Response(BaseModel):
    answer: str = Field(
        description="Answer the user's input"
    )

    summary: str = Field(
        description="Short summary of the answer"
    )


model = ChatGroq(
    model="openai/gpt-oss-20b"
)

structured_model = model.with_structured_output(Response)

user = input("Please enter anything: ")

response = structured_model.invoke(user)

print("Answer:", response.answer)
print("Summary:", response.summary)