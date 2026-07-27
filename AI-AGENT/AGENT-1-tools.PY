from langchain.tools import tool




@tool  #Tool Decorator
def add(a:int,b:int):
    """it will return the sum of the two numbers
       Args
           a: number one 
           b: number two
    """
    return a +b

@tool  #Tool Decorator
def sub(a:int,b:int):
    """it will return the sub of the two numbers
       Args
           a: number one 
           b: number two
    """
    return a -b

result = add.invoke({"a":12,"b":3})

# print(result)

# Now We Need LLM and agent 

from langchain_ollama import ChatOllama
from langchain.agents import create_agent

llm = ChatOllama(
    model="llama3.2"
)

# now create teh agent object

agent = create_agent(
    model = llm,
    tools = [add,sub],
    system_prompt="you always use the tools for the calculations"
)

response = agent.invoke({"message":
                         [{"role":"user", "content":"what is 100+5 "}]})

from langchain.tools import tool




@tool  #Tool Decorator
def add(a:int,b:int):
    """it will return the sum of the two numbers
       Args
           a: number one 
           b: number two
    """
    return a +b

@tool  #Tool Decorator
def sub(a:int,b:int):
    """it will return the sub of the two numbers
       Args
           a: number one 
           b: number two
    """
    return a -b


@tool
def mult(a: int, b: int):
    """Multiply two numbers."""
    return a * b


@tool
def div(a: int, b: int):
    """Divide two numbers."""
    if b == 0:
        return "Division by zero is not allowed."
    return a / b


result = add.invoke({"a":12,"b":3})

# print(result)

# Now We Need LLM and agent 

from langchain_ollama import ChatOllama
from langchain.agents import create_agent

llm = ChatOllama(
    model="llama3.2"
)

# now create teh agent object

agent = create_agent(
    model = llm,
    tools = [add,sub,mult,div],
    system_prompt="you always use the tools for the calculations"
)

data = input("please enter what you want to do: ")

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": data
            }
        ]
    }
)

print(response["messages"][-1].content)
                         

