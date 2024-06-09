from openai import OpenAI
import base64
import requests

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "images/data/img30.jpeg"

# Getting the base64 string
base64_image = encode_image(image_path)


client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "Whats wrong in this image?."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
            }
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "Horse"
        }
      ]
    }
  ],
  temperature=0,
  max_tokens=2,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(response)