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

# URL 설정
url = 'https://uppity.co.kr/esg/'

def get_term_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 모든 카드의 링크 추출
    cards = soup.find_all('a', class_='elementor-post__thumbnail__link')
    links = [card['href'] for card in cards]

    #디버깅
    print(links)
    
    return links

def extract_term_details(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')

    term_title = soup.find('h1', class_='entry-title').get_text()
    term_definition = soup.find('div', class_='entry-content').get_text().strip()
    
    return {
        'term': term_title,
        'definition': term_definition
    }

def generate_quiz(economy_terms):
    term = random.choice(economy_terms)
    prompt = (f"Generate a true or false quiz question based on the following description.\n"
              f"Description: {term['definition']}\n"
              f"Question format: '[Description]', True or False?")

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )

    quiz = response.choices[0].text.strip()
    return quiz

term_links = get_term_links(url)
economy_terms = [extract_term_details(link) for link in term_links]

# 예시 퀴즈 생성
if economy_terms:
    quiz = generate_quiz(economy_terms)
    print(quiz)
else:
    print("No terms found. Please check the URL or HTML structure.")
