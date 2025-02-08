from openai import OpenAI
import os 

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key='api_key',
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
    