from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import os

def deliver_development_task():
    
    #Defining llm
    llm = ChatOpenAI(
        openai_api_base="https://api.groq.com/openai/v1",
        openai_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama3-8b-8192",
        temperature=0.5
    )
    
    #Definining Agents
    manager = Agent(
        role ='IT Project Manager',
        goal='Assign a software development task to your team.',
        backstory='You are a IT Project manager in the Software Develppent Company.',
        verbose=True,
        llm=llm,
        allow_delegation=False
    )
    
    programmer = Agent(
        role ='Python Programmer',
        goal='Write a Python programm for software development task assigned by manager.',
        backstory='You are a Python Programmer in the Software Develppent Company.',
        verbose=True,
        llm=llm,
        allow_delegation=False
    )
    
    quality_assurance = Agent(
        role ='Quality Assurance Tester',
        goal='Perform quality assurance testing on programm written by Python Programmer.',
        backstory='You are a Quality Assurance Tester in the Software Develppent Company.',
        verbose=True,
        llm=llm,
        allow_delegation=False
    )
    
    # Create tasks for the agents
    task_manager = Task(
        description='Plan and assign a software development task to your team.',
        agent=manager,
        expected_output='A thoughtful and well planned software development task.'
    )
    
    task_programmer = Task(
        description='Write a programm for the software development task assigned by manager. Follow best programming guidelines.',
        agent=programmer,
        expected_output='A Python programm for the software development task assigned by manager by following best programming guidelines.'
    )
    
    task_qa = Task(
        description='Perform quality assurance testing on Python programm written by programmer.',
        agent=quality_assurance,
        expected_output='Quality Assurance testing result for the Python programm written by programmer.'
    )
    
    crew = Crew(
    agents=[manager, programmer, quality_assurance],
    tasks=[task_manager, task_programmer, task_qa],
    verbose=True,
    process= Process.sequential
    )

    result = crew.kickoff()

    print(result)
    
    
    
    
    
    