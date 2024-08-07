import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

load_dotenv()
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
model = os.getenv("AZURE_OPENAI_MODEL")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")


token_provider = None
auth_mode = "APIKey"
if not api_key:
    auth_mode = "DefaultAzureCredential"
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )

client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=endpoint,
    azure_ad_token_provider=token_provider
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


print(f"Chat with model {model} @ {endpoint} using {auth_mode}\nPlease type \"exit\" to quit.")
while True:
    message = input("You: ")
    if message.strip().lower() == "exit":
        break
    response = queryGpt(message)
    print("Gpt:", response)

print("Goodbye!")
