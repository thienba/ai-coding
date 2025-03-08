import json
import os
import inspect
from dotenv import load_dotenv
import requests
from pprint import pprint

from openai import OpenAI
from pydantic import TypeAdapter

load_dotenv()

# Implement 3 hàm
def get_current_weather(location: str, unit: str):
    """Get the current weather in a given location"""
    # Hardcoded response for demo purposes
    return "Trời rét vãi nôi, 7 độ C"


def get_stock_price(symbol: str):
    """Get the current stock price for a given symbol"""
    # Không làm gì cả, để hàm trống
    pass


def truncate_content(content: str, max_chars: int = 4000) -> str:
    """Truncate content to a maximum number of characters while keeping whole sentences."""
    if len(content) <= max_chars:
        return content
    
    truncated = content[:max_chars]
    # Find the last period to keep whole sentences
    last_period = truncated.rfind('.')
    if last_period > 0:
        truncated = truncated[:last_period + 1]
    return truncated + "\n[Content truncated due to length...]"


# Bài 2: Implement hàm `view_website`, sử dụng `requests` và JinaAI để đọc markdown từ URL
def view_website(url: str):
    """Get the markdown content of a website using Jina AI Reader"""
    try:
        jina_url = f"https://r.jina.ai/{url}"
        response = requests.get(jina_url)
        response.raise_for_status()
        content = response.text
        return truncate_content(content)
    except requests.RequestException as e:
        return f"Error fetching website: {str(e)}"


# Bài 1: Thay vì tự viết object `tools`, hãy xem lại bài trước, sửa code và dùng `inspect` và `TypeAdapter` để define `tools`
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": inspect.getdoc(get_current_weather),
            "parameters": TypeAdapter(get_current_weather).json_schema()
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": inspect.getdoc(get_stock_price),
            "parameters": TypeAdapter(get_stock_price).json_schema()
        }
    },
    {
        "type": "function",
        "function": {
            "name": "view_website",
            "description": inspect.getdoc(view_website),
            "parameters": TypeAdapter(view_website).json_schema()
        }
    }
]

FUNCTION_MAP = {
    "get_current_weather": get_current_weather,
    "get_stock_price": get_stock_price,
    "view_website": view_website
}

# https://platform.openai.com/api-keys
client = OpenAI(
    base_url="https://api.groq.com/openai/v1", 
    api_key=os.getenv("GROQ_API_KEY")
)

COMPLETION_MODEL = "llama3-8b-8192"

messages = [{
    "role": "user", 
    "content": "Please fetch and summarize the content from this URL: https://tuoitre.vn/cac-nha-khoa-hoc-nga-bao-tu-manh-nhat-20-nam-sap-do-bo-trai-dat-2024051020334196.htm"
}]

print("Bước 1: Gửi message lên cho LLM")
pprint(messages)

response = client.chat.completions.create(
    model=COMPLETION_MODEL,
    messages=messages,
    tools=tools
)

print("Bước 2: LLM đọc và phân tích ngữ cảnh LLM")
pprint(response)

print("Bước 3: Lấy kết quả từ LLM")
assistant_message = response.choices[0].message

if not assistant_message.tool_calls:
    print("LLM provided direct response:")
    print(assistant_message.content)
else:
    tool_call = assistant_message.tool_calls[0]
    print("LLM requested to use tool:")
    pprint(tool_call)
    arguments = json.loads(tool_call.function.arguments)

    print("Bước 4: Executing the requested function")
    function_name = tool_call.function.name
    
    try:
        function_result = FUNCTION_MAP[function_name](**arguments)
        messages.append(assistant_message)
        messages.append({
            "role": "tool",
            "content": function_result,
            "tool_call_id": tool_call.id
        })

        final_response = client.chat.completions.create(
            model=COMPLETION_MODEL,
            messages=messages
        )
        print("\nFinal result:")
        print(final_response.choices[0].message.content)
    except Exception as e:
        print(f"Error processing function {function_name}: {str(e)}")