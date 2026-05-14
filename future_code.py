import requests
from bs4 import BeautifulSoup
import json

url = "https://news.ycombinator.com/"

response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, "html.parser")

titles = soup.select('.titleline')
scores = soup.select('.score')

news_list = []

for i in range(len(titles)):
    title_elem = titles[i]
    score_elem = scores[i] if i < len(scores) else None

    title_text = title_elem.get_text(strip=True)
    points = int(score_elem.get_text().split()[0]) if score_elem else 0

    news_item = {
        'title': title_text,
        'points': points
    }
    news_list.append(news_item)

with open('hn_news.json', 'w', encoding='utf-8') as f:
    json.dump(news_list, f, ensure_ascii=False, indent=4)