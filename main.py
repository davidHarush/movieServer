import os
from dotenv import load_dotenv
import requests
from flask import Flask, request, jsonify

api_key = os.getenv("OPENAI_API_KEY")



def ask_openai_question(api_key, question):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": question}],
        "max_tokens": 100
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

# Example usage
question = "What is the capital of France?"
answer = ask_openai_question(api_key, question)
print(answer)
