from llama_agents import LlamaAgentsClient, AsyncLlamaAgentsClient

client = LlamaAgentsClient("http://127.0.0.1:8001")  # i.e. http://127.0.0.1:8001
task_id = client.create_task("What is the secret fact?")
# <Wait a few seconds>
# returns TaskResult or None if not finished
result = client.get_task_result(task_id)