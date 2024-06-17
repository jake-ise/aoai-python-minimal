import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
model = os.getenv("AZURE_OPENAI_MODEL")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=endpoint
)

history = []


def addHistory(role, content):
    history.append({
        "role": role,
        "content": content
    })


def queryGpt(message):
    addHistory("user", message)
    response = client.chat.completions.create(
        model=model,
        messages=history
    )
    response_message = response.choices[0].message
    addHistory(response_message.role, response_message.content)
    return response_message.content


print(f"Chat with model {model} @ {endpoint} type \"exit\" to quit.")
while True:
    message = input("You: ")
    if message.strip().lower() == "exit":
        break
    response = queryGpt(message)
    print("Gpt:", response)

print("Goodbye!")
