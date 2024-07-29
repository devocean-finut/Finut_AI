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

base_url = 'https://uppity.co.kr/economy-dictionary'
num_pages = 12  # 총 페이지 수
term_links = get_term_links(base_url, num_pages)

print("All extracted links:", term_links)
