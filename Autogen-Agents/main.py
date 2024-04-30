import university as UN
import gradio as gr

def run_generation(question):
    result = UN.get_answer(question)
    result = result.chat_history
    student = "Student: " + result[0]["content"] + "<br /><br />"
    professor = result[1]["name"].replace("_"," ") + ": " + result[1]["content"]
    
    final_result="<html><div style='color:black;font-weight:bold;font-size: 1.25em;'>{}</div><div style='color:#000080;font-weight:bold;font-size: 1.25em;'>{}</div></html>".format(student,professor)
    return final_result
    
if __name__ == "__main__":
    # Gradio UI setup
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column(scale=4):
                user_text = gr.Textbox(placeholder="Write your question here", label="Student Question")
                model_output = gr.HTML(label="LLM Agents Output", show_label=True)
                #button_submit = gr.Button(value="Submit")

        user_text.submit(run_generation, [user_text], model_output)
        #button_submit.click(run_generation, [user_text], model_output)

        demo.queue(max_size=32).launch(server_port=8082)