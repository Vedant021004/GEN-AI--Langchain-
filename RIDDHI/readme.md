# 🧠 LangChain Messages — From Custom Messages to `messages[-1]`

This README explains the fundamentals of **messages in LangChain/LangGraph**, including:

* Custom messages
* `role`
* `content`
* Message lists
* `messages[-1]`
* Getting the latest message
* Difference between a message and message history
* How messages are passed to an agent

---

## 1. What is a Message?

A message represents **one piece of communication** between a user and an AI.

For example:

```python
{
    "role": "user",
    "content": "I am Vedant Kapil"
}
```

It contains two important parts:

```text
role
  ↓
Who sent the message?

content
  ↓
What did they say?
```

---

# 2. `role`

The `role` tells the model **who sent the message**.

Example:

```python
{
    "role": "user",
    "content": "Hello"
}
```

The role is:

```text
user
```

An AI response can be represented as:

```python
{
    "role": "assistant",
    "content": "Hello! How can I help?"
}
```

So:

```text
user       → message from the user
assistant  → message from the AI
```

---

# 3. `content`

`content` contains the **actual message**.

```python
{
    "role": "user",
    "content": "What is Python?"
}
```

Here:

```text
role    → user
content → What is Python?
```

---

# 4. Multiple Messages

A conversation contains multiple messages.

Therefore, we can store them inside a list:

```python
messages = [
    {
        "role": "user",
        "content": "I am Vedant"
    },
    {
        "role": "assistant",
        "content": "Nice to meet you, Vedant!"
    },
    {
        "role": "user",
        "content": "What is Python?"
    }
]
```

The structure is:

```text
messages
│
├── Message 0
│     ├── role
│     └── content
│
├── Message 1
│     ├── role
│     └── content
│
└── Message 2
      ├── role
      └── content
```

---

# 5. Accessing a Message

Python lists use indexes.

```python
messages[0]
```

gets the first message.

```python
messages[1]
```

gets the second message.

```python
messages[2]
```

gets the third message.

---

# 6. What is `messages[-1]`?

`-1` means:

> **The last item in the list.**

Example:

```python
messages = [
    "Hello",
    "How are you?",
    "I am fine"
]
```

Then:

```python
messages[-1]
```

returns:

```text
I am fine
```

The same concept applies to LangChain messages.

```python
messages[-1]
```

means:

> Get the **latest message**.

---

# 7. `messages[-1]` vs `messages[-1].content`

Suppose:

```python
messages = [
    {
        "role": "user",
        "content": "I am Vedant"
    },
    {
        "role": "assistant",
        "content": "Nice to meet you!"
    }
]
```

Then:

```python
messages[-1]
```

gets the entire last message:

```python
{
    "role": "assistant",
    "content": "Nice to meet you!"
}
```

But:

```python
messages[-1]["content"]
```

gets:

```text
Nice to meet you!
```

With LangChain message objects, you commonly see:

```python
messages[-1].content
```

So:

```text
messages[-1]
       ↓
last message

messages[-1].content
       ↓
content of last message
```

---

# 8. Getting the Last Message in an Agent

When an agent returns:

```python
res
```

the response contains messages:

```python
res["messages"]
```

You can get the latest message:

```python
res["messages"][-1]
```

And get its content:

```python
res["messages"][-1].content
```

Therefore:

```python
print(res["messages"][-1].content)
```

means:

> Get the messages → select the last message → get its content → print it.

---

# 9. Passing a Custom Message to an Agent

When you write:

```python
user = input("Ask: ")
```

suppose the user enters:

```text
I am Vedant
```

You can create a message:

```python
message = {
    "role": "user",
    "content": user
}
```

The result becomes:

```python
{
    "role": "user",
    "content": "I am Vedant"
}
```

Then pass it to the agent:

```python
res = agent.invoke(
    {
        "messages": [message]
    }
)
```

---

# 10. Why is `messages` a List?

Notice:

```python
"messages": [message]
```

The square brackets `[]` mean it is a **list**.

This allows multiple messages:

```python
"messages": [
    {
        "role": "user",
        "content": "I am Vedant"
    },
    {
        "role": "assistant",
        "content": "Nice to meet you!"
    }
]
```

So:

```text
message
   ↓
ONE message

messages
   ↓
LIST of messages
```

---

# 11. Custom Message Variable

You can create your own variable:

```python
user_message = {
    "role": "user",
    "content": user
}
```

Then:

```python
res = agent.invoke(
    {
        "messages": [user_message]
    }
)
```

The variable name:

```python
user_message
```

can be anything.

For example:

```python
msg = {
    "role": "user",
    "content": user
}
```

also works.

The important part for the default agent input is the state key:

```python
"messages"
```

---

# 12. Custom Message vs `messages`

This is an important distinction.

You can name your Python variable whatever you want:

```python
my_message = {
    "role": "user",
    "content": "Hello"
}
```

But when using the default LangChain agent state, you pass it through:

```python
{
    "messages": [my_message]
}
```

So:

```text
my_message
     ↓
your Python variable

messages
     ↓
agent's conversation state field
```

---

# 13. Message History

A conversation can look like:

```python
messages = [
    {
        "role": "user",
        "content": "I am Vedant"
    },
    {
        "role": "assistant",
        "content": "Nice to meet you!"
    },
    {
        "role": "user",
        "content": "What is LangGraph?"
    },
    {
        "role": "assistant",
        "content": "LangGraph is..."
    }
]
```

This entire list represents the **conversation history**.

You can access:

```python
messages[0]
```

First message.

```python
messages[-1]
```

Latest message.

```python
messages[-2]
```

Second-last message.

---

# 14. Negative Indexing

Python supports negative indexes:

```text
messages[-1] → last
messages[-2] → second last
messages[-3] → third last
```

Example:

```python
messages = ["A", "B", "C", "D"]
```

```python
messages[0]   # A
messages[1]   # B
messages[-1]  # D
messages[-2]  # C
```

---

# 15. Complete Example

```python
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver


llm = ChatOllama(
    model="llama3.2"
)

memory = MemorySaver()

agent = create_agent(
    model=llm,
    checkpointer=memory
)

config = {
    "configurable": {
        "thread_id": "1"
    }
}


while True:

    user = input("Ask: ")

    if user.lower() == "bye":
        break

    user_message = {
        "role": "user",
        "content": user
    }

    res = agent.invoke(
        {
            "messages": [user_message]
        },
        config=config
    )

    print(
        "AI:",
        res["messages"][-1].content
    )
```

---

# 16. Understand This Line

The most important line is:

```python
res["messages"][-1].content
```

Break it down:

```text
res
 ↓
agent response/state

["messages"]
 ↓
conversation messages

[-1]
 ↓
latest message

.content
 ↓
text inside that message
```

Therefore:

```python
res["messages"][-1].content
```

means:

> **Get the content of the latest message in the agent's conversation.**

---

# 17. Mental Model

Remember this:

```text
STATE
│
└── messages
      │
      ├── Message
      │     ├── role
      │     └── content
      │
      ├── Message
      │     ├── role
      │     └── content
      │
      └── Message
            ├── role
            └── content
```

And:

```text
messages[-1]
      ↓
last Message

messages[-1].content
      ↓
text inside last Message
```

### ⭐ Key takeaway

```python
message
```

= **one message**

```python
messages
```

= **list of messages**

```python
messages[-1]
```

= **last message**

```python
messages[-1].content
```

= **content of the last message**
