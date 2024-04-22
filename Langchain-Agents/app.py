import retriever

if __name__ == "__main__":
    user_message="Whats top news in Japan today?"
    retriever.create_and_invoke_langchain_agents(user_message)