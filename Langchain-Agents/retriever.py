from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_tool_calling_agent, AgentExecutor

def create_and_invoke_langchain_agents():
    loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
    docs = loader.load()
    documents = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200
    ).split_documents(docs)

    vector = FAISS.from_documents(documents, OpenAIEmbeddings())
    retriever = vector.as_retriever()

    retriever.get_relevant_documents("how to upload a dataset")[0]

    """Document(page_content='import Clientfrom langsmith.evaluation import evaluateclient = Client()# Define dataset: these are your test casesdataset_name = "Sample Dataset"dataset = client.create_dataset(dataset_name, description="A sample dataset in LangSmith.")client.create_examples(    inputs=[        {"postfix": "to LangSmith"},        {"postfix": "to Evaluations in LangSmith"},    ],    outputs=[        {"output": "Welcome to LangSmith"},        {"output": "Welcome to Evaluations in LangSmith"},    ],    dataset_id=dataset.id,)# Define your evaluatordef exact_match(run, example):    return {"score": run.outputs["output"] == example.outputs["output"]}experiment_results = evaluate(    lambda input: "Welcome " + input[\'postfix\'], # Your AI system goes here    data=dataset_name, # The data to predict and grade over    evaluators=[exact_match], # The evaluators to score the results    experiment_prefix="sample-experiment", # The name of the experiment    metadata={      "version": "1.0.0",      "revision_id":'
            , metadata={'source': 'https://docs.smith.langchain.com/overview', 'title': 'Getting started with LangSmith | 🦜️🛠️ LangSmith', 'description': 'Introduction', 'language': 'en'})
    """
    retriever_tool = create_retriever_tool(
        retriever,
        "langsmith_search",
        "Search for information about LangSmith. For any questions about LangSmith, you must use this tool!",
    )

    search = TavilySearchResults()
    tools = [search, retriever_tool]

    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

    prompt = hub.pull("hwchase17/openai-functions-agent")
    prompt.messages

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent,tools=tools,verbose=True)

    agent_executor.invoke({"input": "hi!"})

    agent_executor.invoke({"input": "how can langsmith help with testing?"})

