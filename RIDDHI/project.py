from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel
import subprocess

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b"
)


class State(BaseModel):
    question: str
    app: str = ""
    action: str = ""
    query: str = ""
    answer: str = ""


def classifier(state: State):

    r = llm.invoke(
        f"""
        You are a desktop assistant.

        Understand what the user wants and return ONLY this format:

        app|action|query

        Available apps:

        vscode
        spotify
        whatsapp
        chrome
        youtube
        github
        llm

        Available actions:

        open
        search
        play
        none

        Examples:

        User: open vscode
        vscode|open|

        User: open code
        vscode|open|

        User: launch visual studio code
        vscode|open|

        User: open spotify
        spotify|open|

        User: play Parvati on Spotify
        spotify|play|Parvati

        User: search Arijit Singh on Spotify
        spotify|search|Arijit Singh

        User: open whatsapp
        whatsapp|open|

        User: open chrome
        chrome|open|

        User: search LangGraph on Chrome
        chrome|search|LangGraph

        User: search LangGraph tutorial
        chrome|search|LangGraph tutorial

        User: open YouTube
        youtube|open|

        User: play Python tutorial on YouTube
        youtube|play|Python tutorial

        User: search LangGraph tutorial on YouTube
        youtube|search|LangGraph tutorial

        User: open GitHub
        github|open|

        User: what is LangGraph?
        llm|none|

        Return ONLY:
        app|action|query

        User request:
        {state.question}
        """
    )

    result = r.content.strip()

    if "|" not in result:
        return {
            "app": "llm",
            "action": "none",
            "query": ""
        }

    parts = result.split("|", 2)

    app = parts[0].strip().lower()
    action = parts[1].strip().lower()
    query = parts[2].strip()

    return {
        "app": app,
        "action": action,
        "query": query
    }


def decide(state: State):

    if state.app == "vscode":
        return "vscode"

    if state.app == "spotify":
        return "spotify"

    if state.app == "whatsapp":
        return "whatsapp"

    if state.app == "chrome":
        return "chrome"

    if state.app == "youtube":
        return "youtube"

    if state.app == "github":
        return "github"

    return "general_llm"


def open_vscode(state: State):

    subprocess.Popen(
        ["code"]
    )

    return {
        "answer": "VS Code opened successfully."
    }


def open_spotify(state: State):

    subprocess.Popen(
        "start spotify:",
        shell=True
    )

    if state.action == "open":

        return {
            "answer": "Spotify opened successfully."
        }

    if state.action == "search":

        query = state.query.replace(" ", "%20")

        subprocess.Popen(
            f"start spotify:search:{query}",
            shell=True
        )

        return {
            "answer": f"Searching Spotify for {state.query}."
        }

    if state.action == "play":

        query = state.query.replace(" ", "%20")

        subprocess.Popen(
            f"start spotify:search:{query}",
            shell=True
        )

        return {
            "answer": f"Searching Spotify for {state.query}."
        }

    return {
        "answer": "Spotify opened successfully."
    }


def open_whatsapp(state: State):

    subprocess.Popen(
        "start whatsapp:",
        shell=True
    )

    return {
        "answer": "WhatsApp opened successfully."
    }


def open_chrome(state: State):

    if state.action == "open":

        subprocess.Popen(
            ["cmd", "/c", "start", "", "chrome"]
        )

        return {
            "answer": "Chrome opened successfully."
        }

    if state.action == "search":

        query = state.query.replace(" ", "+")

        url = f"https://www.google.com/search?q={query}"

        subprocess.Popen(
            ["cmd", "/c", "start", "", "chrome", url]
        )

        return {
            "answer": f"Searching Chrome for {state.query}."
        }

    return {
        "answer": "Chrome opened successfully."
    }


def open_youtube(state: State):

    if state.action == "open":

        subprocess.Popen(
            ["cmd", "/c", "start", "https://www.youtube.com"]
        )

        return {
            "answer": "YouTube opened successfully."
        }

    if state.action == "search":

        query = state.query.replace(" ", "+")

        url = f"https://www.youtube.com/results?search_query={query}"

        subprocess.Popen(
            ["cmd", "/c", "start", url]
        )

        return {
            "answer": f"Searching YouTube for {state.query}."
        }

    if state.action == "play":

        query = state.query.replace(" ", "+")

        url = f"https://www.youtube.com/results?search_query={query}"

        subprocess.Popen(
            ["cmd", "/c", "start", url]
        )

        return {
            "answer": f"Searching YouTube for {state.query}."
        }

    return {
        "answer": "YouTube opened successfully."
    }


def open_github(state: State):

    subprocess.Popen(
        ["cmd", "/c", "start", "https://github.com"]
    )

    return {
        "answer": "GitHub opened successfully."
    }


def general_llm(state: State):

    r = llm.invoke(
        f"""
        You are a helpful AI assistant.

        Answer the user's question clearly,
        accurately and concisely.

        User question:
        {state.question}
        """
    )

    return {
        "answer": r.content
    }


graph = StateGraph(State)

graph.add_node("classifier", classifier)

graph.add_node("vscode", open_vscode)
graph.add_node("spotify", open_spotify)
graph.add_node("whatsapp", open_whatsapp)
graph.add_node("chrome", open_chrome)
graph.add_node("youtube", open_youtube)
graph.add_node("github", open_github)
graph.add_node("general_llm", general_llm)

graph.add_edge(
    START,
    "classifier"
)

graph.add_conditional_edges(
    "classifier",
    decide,
    {
        "vscode": "vscode",
        "spotify": "spotify",
        "whatsapp": "whatsapp",
        "chrome": "chrome",
        "youtube": "youtube",
        "github": "github",
        "general_llm": "general_llm"
    }
)

graph.add_edge("vscode", END)
graph.add_edge("spotify", END)
graph.add_edge("whatsapp", END)
graph.add_edge("chrome", END)
graph.add_edge("youtube", END)
graph.add_edge("github", END)
graph.add_edge("general_llm", END)

app = graph.compile()


while True:

    question = input("\nAsk: ")

    if question.lower().strip() in ["exit", "quit", "q"]:
        print("Goodbye!")
        break

    result = app.invoke(
        State(
            question=question
        )
    )

    print("\nApp:", result["app"])
    print("Action:", result["action"])
    print("Query:", result["query"])
    print("Answer:", result["answer"])
