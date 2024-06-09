import autogen
import os
import shutil

# Define functions for function-calling
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

def analyze_image(imagename):
    llm_config = {
        "config_list": [{"model": "gpt-4o", "api_key": os.environ["OPENAI_API_KEY"]}],
    }

    # Define Agents
    user_proxy = autogen.UserProxyAgent(
        name="Image Analyzer",
        llm_config=llm_config,
        system_message="""You are an Image analyzer.
                         Call move_to_cats_folder_tool if you find cat in the image, 
                         call move_to_dogs_folder_tool if you find dog in the image,
                         otherwise dont call any function.""",
        human_input_mode="TERMINATE",

    )
    
    cat_user_proxy = autogen.AssistantAgent(
        name="cat_user_proxy",
        system_message="""Move file to cats folder.""",
        human_input_mode="TERMINATE",
        function_map={
            "move_to_cats_folder": move_to_cats_folder
        }
    )
    
    dog_user_proxy = autogen.AssistantAgent(
        name="dog_user_proxy",
        system_message="""Move file to dogs folder.""",
        human_input_mode="TERMINATE",
        function_map={
            "move_to_dogs_folder": move_to_dogs_folder,
        }
    )

    group_chat = autogen.GroupChat(
        agents=[user_proxy,cat_user_proxy,dog_user_proxy], messages=[], max_round=2
    )

    manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=llm_config)
    filepath = "images/data/" + imagename
    user_question = "{}".format(filepath)
    
    response = user_proxy.initiate_chat(
        manager,
        message=user_question,
    )
    
    return response
    
#get_answer("What is the chemical formula for water?")