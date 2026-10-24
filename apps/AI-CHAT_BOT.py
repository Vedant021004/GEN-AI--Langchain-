import logging

import streamlit as st
from langchain_ollama import ChatOllama

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Vedant's Bot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Vedant's Bot")


# Store the model only once
if "llm" not in st.session_state:
    st.session_state.llm = ChatOllama(model="llama3.2")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


with st.sidebar:
    st.title("⚙️ Settings")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


prompt = st.chat_input("Ask anything...")

if prompt:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:
                response = st.session_state.llm.invoke(prompt)
            except Exception as e:
                logger.exception("Ollama invocation failed for prompt: %s", prompt)
                st.error(
                    f"Could not reach the model: {e}\n\n"
                    "Check that Ollama is running and that the llama3.2 model is pulled."
                )
                st.stop()

            st.markdown(response.content)

    # Save AI message
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.content
        }
    )