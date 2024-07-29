import requests
from bs4 import BeautifulSoup

def get_term_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    #모든 카드의 링크 추출
    cards = soup.find_all('div', class_='uc_post_title') #'uc_post_title' 클래스를 가진 모든 <div> 태그를 찾기
    links = [card.find('a')['href'] for card in cards] # 각 <a> 태그에서 href 속성(링크)을 추출하여 리스트에 저장하기

    return links

url = 'https://uppity.co.kr/economy-dictionary/'
term_links = get_term_links(url)  # 링크를 추출하는 함수 호출

print(term_links)