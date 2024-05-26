
from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import BaseTool, FunctionTool

def multiply(a: int, b: int) -> int:
    """Multiple two integers and returns the result integer"""
    return a * b

def add(a: int, b: int) -> int:
    """Add two integers and returns the result integer"""
    return a + b

def divide(a: int, b: int) -> int:
    if(b==0):
        return 0
    return a/b

def substract(a: int,b: int) ->int:
    return a-b

def calculate(query):

    multiply_tool = FunctionTool.from_defaults(fn=multiply,description="Call this function for multiplication.")
    add_tool = FunctionTool.from_defaults(fn=add,description="Call this function for addition.")
    divide_tool= FunctionTool.from_defaults(fn=divide,description="Call this function for division.")
    substract_tool = FunctionTool.from_defaults(fn=substract,description="Call this function for substraction.")
    
    llm = OpenAI(model="gpt-4o")
    agent = OpenAIAgent.from_tools(
        [multiply_tool, add_tool, divide_tool,substract_tool], llm=llm, verbose=True
    )

    response = agent.chat(query)
    print(str(response))