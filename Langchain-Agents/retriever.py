from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_tool_calling_agent, AgentExecutor

def create_and_invoke_langchain_agents(user_message):
    
    #Creating retriever by creating FAISS embedding by reading data from web-page.
    loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
    docs = loader.load()
    documents = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200
    ).split_documents(docs)

    vector = FAISS.from_documents(documents, OpenAIEmbeddings())
    retriever = vector.as_retriever()

    retriever.get_relevant_documents("how to upload a dataset")[0]

    retriever_tool = create_retriever_tool(
        retriever,
        "langsmith_search",
        "Search for information about LangSmith. For any questions about LangSmith, you must use this tool!",
    )

    #Initializing TavilySearchResults object, this will be used for web/internet search.
    search = TavilySearchResults(verbose=False)
    
    #Two tools, "search" is for internet search and "retriever_tool" for vector/semantic search on FIASS vector data. 
    tools = [search, retriever_tool]

    #Initilizing llm using OepnAI gpt-3.5-turbo model.
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

    #Initializing prompt
    prompt = hub.pull("hwchase17/openai-functions-agent")
    prompt.messages

    #Initializing agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    #Initializing AgentExecutor
    agent_executor = AgentExecutor(agent=agent,tools=tools,verbose=False)

    #Invoking AgentExecutor to get response. AgentExecutor will decide which tool to use.
    response = agent_executor.invoke({"input": f"{user_message}"})
    print("User: "+ response["input"])
    print("Agent: "+ response["output"])
    #print("User: " + response.input)
    #print("Agent: " + response.output)

