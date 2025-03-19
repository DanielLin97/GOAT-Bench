import base64
import requests
import json
import time

# OpenAI API Key
api_key = "xxxxxxxxxxxxxxxxx"

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def call_gpt4v(image_path, INSTRUCTION):
    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": INSTRUCTION
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
                }
            ]
            }
        ],
        "max_tokens": 16,
        "temperature": 0.0
    }
    success = False
    re_try_count = 5
    response = ''
    while not success and re_try_count >= 0:
        re_try_count -= 1
        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            success = True
        except Exception as e:
            print(e)
            time.sleep(20)
            print('retry')

    return response