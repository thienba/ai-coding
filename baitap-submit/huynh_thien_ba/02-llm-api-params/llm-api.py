from openai import OpenAI

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key='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',
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