from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    base_url=os.getenv("GROQ_BASE_URL"),
    api_key=os.getenv("GROQ_API_KEY")
)

chat_completion = client.chat.completions.create(
   messages=[
        {
	    # Cài đặt cách trả lời, nhiệm vụ của bot
            "role": "system",
            "content": "You are a friendly and flirty female tour guide.",
        },
        {
	    # Câu hỏi gốc của bạn
            "role": "user",
            "content": "Thủ đô của Pháp là gì?",
        },
        {
	    # Câu trả lời của bot
            "role": "assistant",
            "content": "Thủ đô của Pháp là Paris.",
        },
        {
	    # Câu hỏi tiếp theo của bạn
            "role": "user",
            "content": "Tới đó rồi thì nên đi đâu chơi?",
        }
    ],
    model="gemma2-9b-it",
)

print(chat_completion.choices[0].message.content)

stream = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Hello. Who are you? Write me a long poem to introduce your self.",
        }
    ],
    model="gemma2-9b-it",
    stream=True
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")