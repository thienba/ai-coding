from openai import OpenAI
import os 

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key='api_key',
)

messages = []

while True: 
    print("Welcome to the chatbot!")
    print("--------------------------------")
    print("Type ':q' to exit")
    print("Type ':r' to reset conversation")
    print("--------------------------------")
    user_input = input("Enter your message: ")
    
    if(user_input == ":q"):
        print("Exiting...")
        break
    elif(user_input == ":r"):
        messages = []
        os.system('cls' if os.name == 'nt' else 'clear')
        continue
    
    messages.append({
        "role": "user",
        "content": user_input,
    })

    stream = client.chat.completions.create(
        messages=messages,
        model="gemma2-9b-it",
        stream=True
    )

    print("Assistant: ", end="")    
    assistant_response = ""
    for chunk in stream:
        content = chunk.choices[0].delta.content or ""
        assistant_response += content
        print(content, end="")
    print("\n")
    
    messages.append({
        "role": "assistant",
        "content": assistant_response
    })