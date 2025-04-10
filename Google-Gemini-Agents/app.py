# THIS CODE IS ABSOULUTE BECAUSE GOOGLE GOOGLE CHANGED THEIR GEMINI API
import google.generativeai as genai
import google.ai.generativelanguage as glm
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

def get_order_status(order_id: str) -> str:
    """Fetches the status of a given order ID."""
    # Mock data for example purposes
    order_statuses = {
        "12345": "Shipped",
        "67890": "Processing",
        "11223": "Delivered"
    }
    return order_statuses.get(order_id, "Order ID not found.")

def initiate_return(order_id: str, reason: str) -> str:
    """Initiates a return for a given order ID with a specified reason."""
    # Mock data for example purposes
    if order_id in ["12345", "67890", "11223"]:
        return f"Return initiated for order {order_id} due to: {reason}."
    else:
        return "Order ID not found. Cannot initiate return."

def cancel_order(order_id: str) -> str:
    """Cancels a given order ID if possible."""
    # Mock data for example purposes
    order_statuses = {
        "12345": "Shipped",
        "67890": "Processing",
        "11223": "Delivered"
    }
    if order_id in order_statuses:
        if order_statuses[order_id] == "Processing":
            return f"Order {order_id} has been canceled successfully."
        else:
            return f"Order {order_id} cannot be canceled as it is already {order_statuses[order_id]}."
    else:
        return "Order ID not found. Cannot cancel order."

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash-latest',
    tools=[get_order_status, initiate_return,cancel_order] # list of all available tools
)


chat = model.start_chat(enable_automatic_function_calling=True)

#customer_query = 'What is the status of order 12345?'
#customer_query = 'What is the status of order 999?'
#customer_query = 'I want to return order 11223 because it is defective.'
#response = chat.send_message(customer_query)
#response = chat.send_message('Can you check the status of order 11223? If its delivered, please initiat return as it was the wrong order')
#response = chat.send_message('Can you check the status of order 67890? If its delivered, please initiat return as it was the wrong order else cancel the order.')
response = chat.send_message("What is the status of order 12345? Also, can you cancel order 67890 and initiate a return for order 11223 because it is defective?")
print(response.text)

"""for content in chat.history:
    part = content.parts[0]
    print(content.role, "->", type(part).to_dict(part))
    print('-'*80)"""


