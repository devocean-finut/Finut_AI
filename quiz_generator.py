import openai
import os
import json
import random
from dotenv import load_dotenv

# .env 파일의 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv('OPENAI_API_KEY')

# economy_terms.json 파일에서 데이터를 읽어오기
with open('economy_terms.json', 'r', encoding='utf-8') as f:
    economy_terms = json.load(f)

def generate_quiz(term, description):
    prompt = (f"Generate a true or false quiz question based on the following description.\n"
              f"Term: {term}\n"
              f"Description: {description}\n"
              f"Question format: '[Description]', True or False?")

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )

    quiz = response.choices[0].text.strip()
    return quiz

# 예시 퀴즈 생성
if economy_terms:
    term_info = random.choice(economy_terms)
    quiz = generate_quiz(term_info['term'], term_info['description'])
    print(quiz)
else:
    print("No terms found. Please check the economy_terms.json file.")
