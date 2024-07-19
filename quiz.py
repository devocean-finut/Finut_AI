import openai
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

#.env 파일의 환경변수 로드
load_dorenv()

#환경변수에서 api키 읽기
openai.api_key = os.getenv('OPENAI_API_KEY')

