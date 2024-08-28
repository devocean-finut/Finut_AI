import json
import requests
from bs4 import BeautifulSoup

def get_term_links(base_url, num_pages):
    all_links = []
    for page in range(1, num_pages + 1):
        if page == 1:
            url = base_url #첫 페이지 url
        else:
            url = f"{base_url}/page/{page}/"  # 두 번째 페이지부터의 URL 패턴
        
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 모든 카드의 링크 추출
        cards = soup.find_all('div', class_='uc_post_title')
        links = [card.find('a')['href'] for card in cards]

        # 추출된 링크를 전체 링크 리스트에 추가
        all_links.extend(links)

        # 디버깅: 각 페이지에서 추출된 링크 출력
        #print(f"Extracted links from page {page}: {links}")
    
    return all_links

def extract_term_details(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')

    #용어와 정의 추출
    term_title = soup.find('h2', class_='elementor-heading-title').get_text()
    term_description = " ".join([p.get_text() for p in soup.find_all('p')]).strip()

    return {
        'term': term_title,
        'description': term_description
    }

base_url = 'https://uppity.co.kr/economy-dictionary'
num_pages = 12  # 총 페이지 수
term_links = get_term_links(base_url, num_pages)

#print("All extracted links:", term_links)

#print("1")

# 각 링크에서 용어와 정의를 추출하여 리스트에 저장
economy_terms = [extract_term_details(link) for link in term_links]

# 추출된 용어와 정의 출력
# for term in economy_terms:
#     print(f"Term: {term['term']}\nDescription: {term['description']}\n")

# JSON 파일로 저장
with open('economy_terms.json', 'w', encoding='utf-8') as f:
    json.dump(economy_terms, f, ensure_ascii=False, indent=4)
