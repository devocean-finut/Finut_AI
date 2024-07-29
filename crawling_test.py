import requests
from bs4 import BeautifulSoup
import time

url = 'https://uppity.co.kr/economy-dictionary/'

def get_term_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 모든 카드의 링크 추출
    cards = soup.find_all('a', class_='elementor-post__thumbnail__link')
    links = [card['href'] for card in cards]

    # 디버깅: 추출된 링크 출력
    print("Extracted links: ", links)

    return links

def extract_term_details(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 용어와 정의 추출
    term_title = soup.find('h1', class_='entry-title').get_text()
    term_definition = soup.find('div', class_='entry-content').get_text().strip()
    
    return {
        'term': term_title,
        'definition': term_definition
    }

# URL 설정
term_links = get_term_links(url)

# 각 링크에 접근하여 용어와 정의 추출
economy_terms = []
for link in term_links:
    details = extract_term_details(link)
    economy_terms.append(details)
    time.sleep(1)  # 사이트에 부하를 주지 않기 위해 요청 간 간격을 둠

# 추출된 용어와 정의 출력
for term in economy_terms:
    print(f"Term: {term['term']}\nDefinition: {term['definition']}\n")

# 예시 퀴즈 생성 함수
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

# 예시 퀴즈 생성
if economy_terms:
    quiz = generate_quiz(economy_terms)
    print(quiz)
else:
    print("No terms found. Please check the URL or HTML structure.")