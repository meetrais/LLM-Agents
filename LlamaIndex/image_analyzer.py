
from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import BaseTool, FunctionTool
import shutil
import os
from os import path

def move_to_cats_folder(imagepath: str):
    filename = os.path.basename(imagepath)
    src= imagepath
    dest= "images/cats/" + filename
    shutil.move(src, dest)

def move_to_dogs_folder(imagepath: str):
    filename = os.path.basename(imagepath)
    src= imagepath
    dest= "images/dogs/" + filename
    shutil.move(src, dest)

def move_to_horse_folder(imagepath: str):
    filename = os.path.basename(imagepath)
    src= imagepath
    dest= "images/horse/" + filename
    shutil.move(src, dest)

def analyze(imagename):

    move_to_cats_folder_tool = FunctionTool.from_defaults(fn=move_to_cats_folder,
                                                          description="Function to call if image has cat.")
    
    move_to_dogs_folder_tool = FunctionTool.from_defaults(fn=move_to_dogs_folder,
                                                          description="Function to call if image has dog.")
    
    move_to_horse_folder_tool = FunctionTool.from_defaults(fn=move_to_horse_folder,
                                                          description="Function to call if image has horse.")
    
    llm = OpenAI(model="gpt-4o")
    agent = OpenAIAgent.from_tools(
        [move_to_cats_folder_tool, move_to_dogs_folder_tool], llm=llm, verbose=True,
        system_prompt="""Call move_to_cats_folder_tool if you find cat, 
                         call move_to_dogs_folder_tool if you find dog,
                         otherwise dont call any function.
                        """
    )    
    imagepath = path.relpath("images/data/" + imagename)

    response = agent.chat(imagepath)
    print(str(response))