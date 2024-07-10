from llama_index.llms.ollama import Ollama
llm = Ollama(model="llama3")
llm.complete("Why is the sky blue?")