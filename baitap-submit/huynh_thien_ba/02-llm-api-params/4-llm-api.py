from pathlib import Path
import openai
from typing import List, Optional

class DocumentTranslator:
    def __init__(self, base_url: str, api_key: str, text_size: int = 2000):
        self.base_url = base_url
        self.api_key = api_key
        self.text_size = text_size
        self.client = openai.OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )

    def split_text(self, text: str) -> List[str]:
        sentences =  text.split('.')
        chunks = []
        current_chunk = []
        current_size = 0
        
        for sentence in sentences:
            sentence_size = len(sentence)
            if current_size + sentence_size > self.text_size:
                chunks.append('. '.join(current_chunk) + '.')
                current_chunk = [sentence]
                current_size = sentence_size
            else:
                current_chunk.append(sentence)
                current_size += sentence_size
        
        if current_chunk:
            chunks.append('. '.join(current_chunk) + '.')
        return chunks
    
    def create_translation_prompt(self, text: str, source_language: str, target_language: str, tone: Optional[str] = None, style: Optional[str] = None) -> str:
        prompt = f"""Translate the following text from {source_language} to {target_language}.

        Text to translate:
        {text}

        Requirements:
        1. Maintain the original meaning and context
        2. Preserve any technical terms or proper nouns
        3. Keep formatting and special characters"""

        if tone:
            prompt += f"\n4. Use a {tone} tone"
        if style:
            prompt += f"\n5. Write in {style} style"

        prompt += "\n\nTranslation:"
        return prompt
    
    def translate_text(self, text: str, source_language: str, target_language: str, tone: Optional[str] = None, style: Optional[str] = None) -> str:
        prompt = self.create_translation_prompt(text, source_language, target_language, tone, style)
        response = self.client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()

    def translate_file(self, file_path: str, output_path: str, source_language: str, target_language: str, tone: Optional[str] = None, style: Optional[str] = None) -> str:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            
        chunks = self.split_text(text)
        translated_texts = []

        for i, chunk in enumerate(chunks, 1):
            print(f"Translating chunk {i} of {len(chunks)}...")
            translated_text = self.translate_text(chunk, source_language, target_language, tone, style)
            translated_texts.append(translated_text)
            
        final_translation = '\n'.join(translated_texts)

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(final_translation)

        print(f"Translation complete. Output saved to {output_path}")
    
    

base_url="https://api.groq.com/openai/v1"
api_key='api_key'

translator = DocumentTranslator(base_url, api_key)
translator.translate_file('input.txt', 'output.txt', 'en', 'vi', tone='formal', style='technical')