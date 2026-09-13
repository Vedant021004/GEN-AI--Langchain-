from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# 1. Define State
class State(TypedDict):
    age: int
    result: str


# 2. Normal node
def check_age(state: State):
    return {}


# 3. Router / decision function
def router(state: State):

    if state["age"] >= 18:
        return "adult"

    return "minor"


# 4. Adult node
def adult(state: State):
    return {
        "result": "You are an adult"
    }


# 5. Minor node
def minor(state: State):
    return {
        "result": "You are a minor"
    }


# 6. Create graph
graph = StateGraph(State)


# 7. Add nodes
graph.add_node("check_age", check_age)
graph.add_node("adult", adult)
graph.add_node("minor", minor)


# 8. Start
graph.add_edge(START, "check_age")


# 9. Conditional edge
graph.add_conditional_edges(
    "check_age",
    router,
    {
        "adult": "adult",
        "minor": "minor"
    }
)


# 10. End
graph.add_edge("adult", END)
graph.add_edge("minor", END)


# 11. Compile
app = graph.compile()


# 12. Run
result = app.invoke({
    "age": 20,
    "result": ""
})


print(result)