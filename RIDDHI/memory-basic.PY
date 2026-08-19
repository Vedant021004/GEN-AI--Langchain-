# from dotenv import load_dotenv
# load_dotenv()

# from langchain_groq import ChatGroq


# llm = ChatGroq(
#     model="openai/gpt-oss-20b"
# )

# while True:

#     user = input("Ask Me...")

#     data = llm.invoke(user)

#     print("AI", data.content)

# while True:

#     memory = []
#     user = input("please ask me anything...")
#     memory.append(user)

#     print(memory)

memory = {}

while True:

    user = input("You: ")

    if user == "bye":
        break

    # Save identity
    if "my name is" in user.lower():
        name = user.lower().replace("my name is", "").strip()
        memory["name"] = name

    elif "i am" in user.lower():
        name = user.lower().replace("i am", "").strip()
        memory["name"] = name

    # Retrieve identity
    if "who am i" in user.lower():
        if "name" in memory:
            print("AI:", f"You are {memory['name']}.")
        else:
            print("AI: I don't know your name yet.")

