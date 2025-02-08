import openai
from pathlib import Path
import subprocess

class ProgrammingTutor:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.client = openai.OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )

    def create_prompt(self, language: str, task: str) -> str:
        return f"""Write a {language} solution for the following programming problem.
        Important: Provide ONLY the raw code without code block indicators, or explanations.
        Do not include ```{language} or ``` tags
        
        Problem:
        {task}

        Requirements:
        1. Use clear variable names
        2. Include necessary imports
        3. Add brief inline comments for complex logic
        4. Handle basic error cases
        5. The code must be directly executable

        Write the code now:"""
    
    def generate_code(self, language: str, task: str) -> str:
        prompt = self.create_prompt(language, task)
        response = self.client.chat.completions.create(
            model="gemma2-9b-it",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    
    def save_code(self, code: str, file_name: str):
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(code)
        print(f"File code saved to {file_name}")

    def run_code(self, language: str, file_name: str):
        if language == 'python':
            subprocess.run(['python', file_name])
        elif language == 'javascript':
            subprocess.run(['node', file_name])
        else:
            print(f"Unsupported language: {language}")

base_url="https://api.groq.com/openai/v1"
api_key='api_key'

tutor = ProgrammingTutor(base_url, api_key)

input_task = input("Enter the task: ")

code = tutor.generate_code('javascript', input_task)
tutor.save_code(code, 'final.js')
tutor.run_code('javascript', 'final.js')