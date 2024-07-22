import openai
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import random

#.env 파일의 환경변수 로드
load_dotenv()

#환경변수에서 api키 읽기
openai.api_key = os.getenv('OPENAI_API_KEY')

def extract_terms(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    terms = soup.find_all('h2', class_='term-tittle')
    definitions = soup.find_all('p', class_='term-description')

    economy_terms = []
    

    for term, definition in zip(terms, definitions):
        economy_terms.append({
            'term': term.get_text(),
            'definition': definition.get_text()
        })
    
    return economy_terms

#퀴즈를 생성하는 함수
def generate_quiz(economy_terms):
    term = random.choice(economy_terms)
    promt = (f"Generate a true or false quiz question based on the following description.\n"
              f"Description: {term['definition']}\n"
              f"Question format: '[Description]', True or False?")
    # 
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )

    quiz = response.choices[0].text.strip()
    return quiz

#url 설정
url = 'https://uppity.co.kr/economy-dictionary/'
economy_terms = extract_terms(url)

#예시 퀴즈 생성
quiz = generate_quiz(economy_terms)
print(quiz)

