# `genai_shared`

This package contains the small reusable pieces shared by the LangChain
learning scripts in this repository. Install it from the repository root with
`pip install -e .`, then scripts can import its modules:

- `llms.py`: Groq, Ollama, and Hugging Face model factories.
- `chat.py`: command-line chat loops, message payloads, and responders.
- `math_tools.py` and `demo_tools.py`: arithmetic and deterministic demo tools.
- `graphs.py`: standard LangGraph tool-calling state and graph wiring.
- `rag.py`: PDF chunking, Chroma construction, and document formatting.
- `sql_agents.py`: SQL database connection and agent construction helpers.
