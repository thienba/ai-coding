from openai import OpenAI
import requests
from bs4 import BeautifulSoup

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key='api_key',
)

def get_website_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        main_content = soup.find('div', {'id': 'main-detail'})
        
        if main_content:
            content = ' '.join([p.text.strip() for p in main_content.find_all('p')])
            return content
        return "Could not find main content"
    
    except requests.RequestException as e:
        return f"Error fetching website: {str(e)}"

def summarize_content(content):
    prompt = f"""Please provide a concise summary of the following article in Vietnamese. 
    Focus on the main points and key information:

    {content}
    
    Summary:"""
    
    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            # max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def main():
    url = input("Enter the URL of the article: ")
    
    content = get_website_content(url)
    
    if content:
        summary = summarize_content(content)
        print("\nSummary of the article:")
        print(summary)
    else:
        print("Cannot get content from this URL.")

main()