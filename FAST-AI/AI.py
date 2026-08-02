from dotenv import load_dotenv
import streamlit as st

from langchain_groq import ChatGroq
from langchain_community.tools import GoogleSerperRun
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
import os





if "memory" not in st.session_state:
    st.session_state.memory = MemorySaver()

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- LLM ---------------- #

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    
)

# ---------------- Tools ---------------- #

search = GoogleSerperRun()

# ---------------- Agent ---------------- #

agent = create_agent(
    model=llm,
    tools=[search],
    system_prompt="""
You are a helpful AI assistant.

Rules:
- Answer in 1-3 sentences.
- Be concise.
- Use Google Search only for current events, news, weather, sports, prices, or information that changes over time.
- Never call Google Search with an empty query.
- If the answer can be given from your own knowledge, do not use Google Search.
""",
    checkpointer=st.session_state.memory,
)

# ---------------- UI ---------------- #

st.set_page_config(
    page_title="Vedant AI",
    page_icon="🤖"
)

st.title("🤖 Vedant's AI Chatbot")

# ---------------- Chat History ---------------- #

for message in st.session_state.history:
    role = message["role"]
    content = message["content"]

    st.chat_message(role).markdown(content)

# ---------------- Chat Input ---------------- #

question = st.chat_input("Ask Anything...")

if question:

    # Display User Message
    st.chat_message("user").markdown(question)

    # Save User Message
    st.session_state.history.append(
        {
            "role": "user",
            "content": question
        }
    )

    try:

        res = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            },
            config={
                "configurable": {
                    "thread_id": "1"
                }
            }
        )

        answer = res["messages"][-1].content

        # Display Assistant Message
        st.chat_message("assistant").markdown(answer)

        # Save Assistant Message
        st.session_state.history.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    except Exception as e:
        st.error(e)