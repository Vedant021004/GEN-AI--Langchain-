# 🤖 Vedant's AI Chatbot.

A simple AI chatbot built using **Streamlit**, **LangChain**, and **Ollama**. This chatbot runs **locally** using the **Llama 3.2** model, allowing users to chat with an AI assistant without relying on cloud APIs.

---

## 🚀 Features

* 💬 ChatGPT-like interface
* 🧠 Powered by Llama 3.2 via Ollama
* ⚡ Built with LangChain
* 📝 Chat history using Streamlit Session State
* 🔄 Real-time conversation
* 🗑️ Clear chat functionality
* 💻 Runs completely offline
* 🎨 Clean and responsive UI

---

## 🛠️ Tech Stack

| Technology | Purpose              |
| ---------- | -------------------- |
| Python     | Programming Language |
| Streamlit  | Web Interface        |
| LangChain  | LLM Framework        |
| Ollama     | Local LLM Runtime    |
| Llama 3.2  | Language Model       |

---

## 📂 Project Structure

```text
Vedants-AI-Chatbot/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/Vedants-AI-Chatbot.git

cd Vedants-AI-Chatbot
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
```

---

### 3️⃣ Activate Environment

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

---

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 5️⃣ Install Ollama

Download Ollama from

[https://ollama.com](https://ollama.com)

---

### 6️⃣ Download Llama 3.2

```bash
ollama pull llama3.2
```

Verify installation

```bash
ollama list
```

---

## ▶️ Run the Project

```bash
streamlit run app.py
```

Your chatbot will open automatically in your browser.

---

## 💬 How It Works

```text
User Question
      │
      ▼
Streamlit UI
      │
      ▼
Session State
      │
      ▼
LangChain
      │
      ▼
Ollama
      │
      ▼
Llama 3.2
      │
      ▼
AI Response
      │
      ▼
Display in Chat Interface
```

---

## 📸 Demo

```
🤖 Vedant's Bot

User:
What is Machine Learning?

-----------------------------------

🤖 Vedant's Bot

Machine Learning is a branch of Artificial Intelligence
that enables computers to learn patterns from data
without being explicitly programmed.
```

---

## 📦 Requirements

```text
streamlit
langchain
langchain-ollama
ollama
```

Install manually

```bash
pip install streamlit langchain langchain-ollama
```

---

## 🧠 Concepts Used

* Streamlit
* Session State
* Chat Interface
* LangChain
* ChatOllama
* Local LLM
* Prompt Engineering

---

## 🌟 Future Improvements

* 🎙️ Voice Assistant
* 📄 PDF Chat (RAG)
* 🖼️ Image Understanding
* 🧠 Memory Support
* 🌐 Multiple LLM Selection
* 🔍 Web Search Integration
* 📥 Export Chat
* 🌙 Dark / Light Theme
* ⚡ Streaming Responses
* 📊 Token Usage Analytics

---

## 📖 Learning Outcomes

Through this project, you will understand:

* Building AI applications with Streamlit
* Integrating LangChain with Ollama
* Running LLMs locally
* Managing chat history using Session State
* Creating interactive AI interfaces

---

## ⭐ If you found this project helpful

Give this repository a ⭐ and feel free to contribute!

---

## 👨‍💻 Author

**Vedant Kapil**

* 💼 Aspiring AI Engineer
* 🧠 Machine Learning Enthusiast
* 🚀 Building AI, LLM, RAG & Automation Projects

GitHub: **[https://github.com/Vedant021004](https://github.com/Vedant021004)**

LinkedIn: **[https://www.linkedin.com/in/vedant-kapil-8a786740a/](https://www.linkedin.com/in/vedant-kapil-8a786740a/)**
