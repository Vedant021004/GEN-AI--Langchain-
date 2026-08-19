from langchain.agents import create_agent

from genai_shared.llms import ollama_llm
from genai_shared.math_tools import MATH_TOOLS, add


llm = ollama_llm()

agent = create_agent(
    model=llm,
    tools=MATH_TOOLS,
    system_prompt="you always use the tools for the calculations",
)

result = add.invoke({"a": 12, "b": 3})

data = input("please enter what you want to do: ")

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": data,
            }
        ]
    }
)

print(response["messages"][-1].content)
