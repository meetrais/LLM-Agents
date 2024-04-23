from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from langchain_openai import ChatOpenAI
from crewai_tools.tools import FileReadTool
import os

def student_asks_question_to_professors():
    
    #Defining llm
    llm = ChatOpenAI(
        openai_api_base="https://api.groq.com/openai/v1",
        openai_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama3-8b-8192",
        temperature=0.5
    )
    
    #Definining Agents
    student = Agent(
        role ='Student',
        goal='Ask question to Professors to get clarity on any random University subject.',
        backstory='You are a Student of well known University of USA.',
        verbose=True,
        llm=llm,
        allow_delegation=False
    )
    
    professor_boilogy = Agent(
        role='Professor of Biology',
        goal='As a professor of Biology answer question of student only if its related to Biology subject. If question is not related to Biology then just say Sorry, this is not my subject.',
        backstory='You are a Professor of Biology. You are subject matter expert of Biology. Many students in the University ask you question on Biology subject',
        verbose=True,
        llm=llm,
        allow_delegation=False
    )
    
    professor_mathematics = Agent(
        role='Professor of Mathematics',
        goal= 'As a professor of Mathematics answer question of student only if its related to Mathematics subject. If question is not related to Mathematics then just say Sorry, this is not my subject.',
        backstory='You are a Professor of Mathematics. You are subject matter expert of Mathematics. Many students in the University ask you question on Mathematics subject',
        verbose=True,
        llm=llm,
        allow_delegation=False
    )
    
    professor_chemistry = Agent(
        role='Professor of Chemistry',
        goal= 'As a professor of Chemistry answer question of student only if its related to Chemistry subject.  If question is not related to Chemistry then just say Sorry, this is not my subject.',
        backstory='You are a Professor of Chemistry. You are subject matter expert of Chemistry. Many students in the University ask you question on Chemistry subject',
        verbose=True,
        llm=llm,
        allow_delegation=False
    )
    
    #Creating Tasks for the agents
    task_student= Task(
        description="As a Univerisity Student ask question to Professors on any random University subject.",
        agent=student,
        expected_output='A question on any random University subject.'
    )
    
    task_professor_biology= Task(
        description="As a Univerisity Professor of Biology answer question only if its related to Biology.",
        agent=professor_boilogy,
        expected_output='An answer only if student asked question about Biology.'
    )
    
    task_professor_mathematics= Task(
        description="As a Univerisity Professor of Mathematics answer question only if its related to Mathematics.",
        agent=professor_mathematics,
        expected_output='An answer only if student asked question about Mathematics.'
    )
    
    task_professor_chemistry= Task(
        description="As a Univerisity Professor of Chemistry answer question only if its related to Chemistry.",
        agent=professor_chemistry,
        expected_output='An answer only if student asked question about Chemistry.'
    )
    
    crew = Crew(
        agents=[student,professor_boilogy,professor_mathematics,professor_chemistry],
        tasks=[task_student,task_professor_biology,task_professor_mathematics,task_professor_chemistry],
        verbose=True,
        process=Process.sequential
    )
    
    result= crew.kickoff()
    
    print(result)
    
    
    