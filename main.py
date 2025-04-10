import requests
import bs4
import lxml
from pprint import pprint
from datetime import datetime

keywords = ['дизайн', 'фото', 'web', 'python']
url = r'https://habr.com/ru/articles/'
habr_url = r'https://habr.com'

def search_keywords(link: str, keywords: list) -> bool:
    response = requests.get(link)
    root = bs4.BeautifulSoup(response.text, features='lxml')
    article_text = root.find('div', attrs={'id' : 'post-content-body'}).text
    for keyword in keywords:
        if keyword in article_text:
            return True

def main():
    response = requests.get(f'{url}')
    root = bs4.BeautifulSoup(response.text, features='lxml')
    articles = root.find_all('article', attrs={'class': 'tm-articles-list__item'})

    for article in articles:
        format = '%Y-%m-%dT%H:%M:%S.%fZ'
        date = datetime.strptime(article.find('time')['datetime'], format)
        date_str = date.strftime('%Y-%m-%d %H:%M:%S') 

        title = article.find('h2', attrs={'class': 'tm-title'}).text
        link = habr_url + article.find('a', attrs={'class' : 'tm-article-datetime-published tm-article-datetime-published_link'})['href']
        
        if search_keywords(link, keywords):
            print(f'{date_str} - {title} - {link}')

if __name__ == '__main__':
    main()