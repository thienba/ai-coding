# 1. Dùng chunking để làm bot trả lời tiểu sử người nổi tiếng, anime v...v
#   - <https://en.wikipedia.org/wiki/S%C6%A1n_T%C3%B9ng_M-TP>
#   - <https://en.wikipedia.org/wiki/Jujutsu_Kaisen>

import os
from dotenv import load_dotenv
from wikipediaapi import Wikipedia
from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions

load_dotenv()

# Function to get Wikipedia content and process it
def get_wiki_content(topic):
    wiki = Wikipedia('HocCodeAI/0.0 (https://hoccodeai.com)', 'en')
    page = wiki.page(topic)
    if not page.exists():
        return None
    return page.text

# Function to chunk text into paragraphs
def chunk_text(text):
    return text.split('\n\n')

# Function to create or get collection
def get_collection(name):
    try:
        return client.get_collection(name=name, embedding_function=embedding_function)
    except:
        return client.create_collection(name=name, embedding_function=embedding_function)

# Initialize ChromaDB
client = chromadb.PersistentClient(path="./data")
client.heartbeat()

# Mặc định, chroma DB sử dụng `all-MiniLM-L6-v2` của Sentence Transformers
# mà mình đã hướng dẫn ở bài trước để tạo embeddings.
embedding_function = embedding_functions.DefaultEmbeddingFunction()

# Ngoài ra, bạn có thể sử dụng mô hình embedding của OpenAI để có hiệu suất tốt hơn
# Nhưng cần đăng ký và có API key của OpenAI
# embedding_function = embedding_functions.OpenAIEmbeddingFunction(api_key=OPENAI_API_KEY, model_name="text-embedding-3-small")

# Initialize OpenAI client
client_openai = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=os.getenv("GROQ_API_KEY"))

# List of topics to index
topics = ["Nguyễn_Nhật_Ánh", "Sơn_Tùng_M-TP", "Jujutsu_Kaisen"]

# Function to create a valid collection name
def create_valid_collection_name(topic):
    # Replace Vietnamese characters with ASCII equivalents
    replacements = {
        'ư': 'u', 'ơ': 'o', 'à': 'a', 'á': 'a', 'ạ': 'a', 'ả': 'a', 'ã': 'a',
        'â': 'a', 'ầ': 'a', 'ấ': 'a', 'ậ': 'a', 'ẩ': 'a', 'ẫ': 'a',
        'ă': 'a', 'ằ': 'a', 'ắ': 'a', 'ặ': 'a', 'ẳ': 'a', 'ẵ': 'a',
        'è': 'e', 'é': 'e', 'ẹ': 'e', 'ẻ': 'e', 'ẽ': 'e',
        'ê': 'e', 'ề': 'e', 'ế': 'e', 'ệ': 'e', 'ể': 'e', 'ễ': 'e',
        'ì': 'i', 'í': 'i', 'ị': 'i', 'ỉ': 'i', 'ĩ': 'i',
        'ò': 'o', 'ó': 'o', 'ọ': 'o', 'ỏ': 'o', 'õ': 'o',
        'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ộ': 'o', 'ổ': 'o', 'ỗ': 'o',
        'ờ': 'o', 'ớ': 'o', 'ợ': 'o', 'ở': 'o', 'ỡ': 'o',
        'ù': 'u', 'ú': 'u', 'ụ': 'u', 'ủ': 'u', 'ũ': 'u',
        'ừ': 'u', 'ứ': 'u', 'ự': 'u', 'ử': 'u', 'ữ': 'u',
        'ỳ': 'y', 'ý': 'y', 'ỵ': 'y', 'ỷ': 'y', 'ỹ': 'y',
        'đ': 'd',
    }
    
    result = topic.lower().replace("_", "").replace("-", "")
    for vietnamese, ascii in replacements.items():
        result = result.replace(vietnamese, ascii)
    
    # Ensure the name only contains valid characters
    import re
    result = re.sub(r'[^a-zA-Z0-9_-]', '', result)
    
    return result

# Process each topic
for topic in topics:
    print(f"Processing {topic}...")
    
    # Get content from Wikipedia
    content = get_wiki_content(topic)
    if not content:
        print(f"Could not find Wikipedia page for {topic}")
        continue
    
    # Create collection for this topic with a valid name
    collection_name = create_valid_collection_name(topic)
    collection = get_collection(collection_name)
    
    # Chunk the content
    paragraphs = chunk_text(content)
    
    # Add chunks to collection
    for index, paragraph in enumerate(paragraphs):
        if paragraph.strip():  # Skip empty paragraphs
            collection.add(documents=[paragraph], ids=[f"{topic}_{index}"])
    
    print(f"Added {len(paragraphs)} paragraphs for {topic}")

# Function to answer questions
def answer_question(topic, question):
    collection_name = create_valid_collection_name(topic)
    try:
        collection = client.get_collection(name=collection_name, embedding_function=embedding_function)
    except:
        return f"No information available for {topic}"
    
    # Query the collection
    results = collection.query(query_texts=[question], n_results=3)
    context = "\n\n".join(results["documents"][0])
    
    prompt = f"""
    Use the following CONTEXT to answer the QUESTION about {topic.replace('_', ' ')}.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Use an unbiased and journalistic tone.

    CONTEXT: {context}

    QUESTION: {question}
    """
    
    # Get response from LLM
    response = client_openai.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "user", "content": prompt},
        ]
    )
    
    return response.choices[0].message.content

# Interactive chatbot
def run_chatbot():
    print("Welcome to the Biography Chatbot!")
    print("Available topics: Nguyễn Nhật Ánh, Sơn Tùng M-TP, Jujutsu Kaisen")
    
    while True:
        topic = input("\nEnter a topic (or 'quit' to exit): ")
        if topic.lower() == 'quit':
            break
            
        # Convert input to Wikipedia format
        wiki_topic = topic.replace(" ", "_")
        
        # Map common variations to our indexed topics
        topic_map = {
            "nguyen_nhat_anh": "Nguyễn_Nhật_Ánh",
            "son_tung": "Sơn_Tùng_M-TP",
            "son_tung_m-tp": "Sơn_Tùng_M-TP",
            "jujutsu_kaisen": "Jujutsu_Kaisen",
            "jujutsu": "Jujutsu_Kaisen"
        }
        
        wiki_topic = topic_map.get(wiki_topic.lower(), wiki_topic)
        
        if wiki_topic not in topics:
            print(f"Sorry, I don't have information about {topic}. Please choose from the available topics.")
            continue
            
        question = input(f"What would you like to know about {topic}? ")
        print("\nThinking...")
        answer = answer_question(wiki_topic, question)
        print(f"\nAnswer: {answer}")

# Run the chatbot
run_chatbot()