import autogen
import os

llm_config = {
    "config_list": [{"model": "gpt-3.5-turbo", "api_key": os.environ["OPENAI_API_KEY"]}],
}

# Define Agents

user_proxy = autogen.UserProxyAgent(
    name="University_Coordinator",
    system_message="""A human user. select most appropriate assistant agent amongst Biology_Professor, Mathematics_Professor, Electronics_Professor
        and Chemistry_Professor to get answer on question asked by user.""",
    human_input_mode="TERMINATE",
)

professor_boilogy = autogen.AssistantAgent(
    name="Biology_Professor",
    llm_config=llm_config,
    system_message="""Professor of Biology. YAs a professor of Biology answer question of student only if its related to Biology subject. 
        If question is not related to Biology then only say Sorry, this is not my subject.""",
)

professor_mathematics = autogen.AssistantAgent(
    name="Mathematics_Professor",
    llm_config=llm_config,
    system_message="""Professor of Mathematics. As a professor of Mathematics answer question of student only if its related to Mathematics subject. 
        If question is not related to Mathematics then only say Sorry, this is not my subject.""",
)

professor_chemistry = autogen.AssistantAgent(
    name="Chemistry_Professor",
    system_message="""Professor of Mathematics. As a professor of Chemistry answer question of student only if its related to Chemistry subject.  
        If question is not related to Chemistry then only say Sorry, this is not my subject.""",
    llm_config=llm_config,
)

professor_electronics = autogen.AssistantAgent(
    name="Electronics_Professor",
    system_message="""Professor of Electronics. As a professor of Electronics answer question of student only if its related to Electronics subject.  
        If question is not related to Electronics then only say Sorry, this is not my subject.""",
    llm_config=llm_config,
)

group_chat = autogen.GroupChat(
    agents=[user_proxy, professor_boilogy, professor_mathematics, professor_chemistry, professor_electronics], messages=[], max_round=2
)
manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=llm_config)

user_proxy.initiate_chat(
    manager,
    message="""What is the chemical formula for water?""",
)