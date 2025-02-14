from openai import OpenAI
import os 
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    base_url=os.getenv("GROQ_BASE_URL"),
    api_key=os.getenv("GROQ_API_KEY")
)

messages = [
    {
        "role": "system",
        "content": "You are a friendly helper.",
    },
]

print("Welcome to the chatbot!")
print("--------------------------------")
user_input = input("Enter your message: ")

messages.append({
    "role": "user",
    "content": user_input,
})

stream = client.chat.completions.create(
    messages=messages,
    model="gemma2-9b-it",
    stream=True
)

for chunk in stream:
    content = chunk.choices[0].delta.content or ""
    print(content, end="")
    