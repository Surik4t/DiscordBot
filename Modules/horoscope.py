import requests, pandas
from bs4 import BeautifulSoup as bs
import asyncio

URL = 'https://horo.mail.ru/prediction/'

def parse(text):
    soup = bs(text, 'html.parser')
    data = soup.find('div', class_='article__item article__item_alignment_left article__item_html').get_text()
    return data
async def get_horoscope(zodiac_sign):
    url_head = f'{zodiac_sign}/today/'
    answer = requests.get(url=URL + url_head)
    if answer.status_code != 200:
        return answer.status_code
    return answer.text

#text = asyncio.run(get_horoscope('libra'))
#parse(text)