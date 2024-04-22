# Langchain Agents Reference
https://www.langchain.com/agents  
https://python.langchain.com/docs/modules/agents/concepts/  

## Commands to run in your terminal. Restart your IDE once after execution.
export LANGCHAIN_TRACING_V2="true"  
export LANGCHAIN_API_KEY="<your-api-key>"  
export TAVILY_API_KEY="<your-tavily-key>"  
export OPENAI_API_KEY="<your-openai-key>"  

Note - if you are on Windows OS then use syntax -> setx Variable-Name Variable-Vlaue  

## Dependencies
Please install dependency libraries specified in Requirements.txt by running this in IDE terminsl -> pip install -r Requirwmwnts.txt

## Overview
There are two Tools for Agent defined in this Programm.  
1) One using tavily_search
2) Another using retriewer which is based on FAISS embedding for LangSmith documentation.

Based on user_message, this Langchain-Agent and LLM based progrram identifies which Tool/Agent to invoke to get answer.  
If user_message is enquiring something which needs interner search then AgentExecutor invokes Tool #1.  
If user_message is enquiring about LangSmith/Langchain/LLMs which is related to FAISS embedding we created for angSmith  
documentation then AgentExecutor will invoke Tool #2.  