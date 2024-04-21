from langchain_community.tools.tavily_search import TavilySearchResults

search = TavilySearchResults()
response = search.invoke("what is the weather in SF")
print(response[1])