import requests
import json
import hashlib
import os
from bs4 import BeautifulSoup
import stat


def compute_MD5_hash(string):

    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


def get_soup(request_url):
    page = requests.get(request_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup


def get_all_news_url(soup):

    news_list = soup.find_all("div", class_="article news-bn first default")
    article_url_list = []

    for i in range(len(news_list)):
      for link in news_list[i].find_all('a'):
        article_url_list.append(link.get('href'))

    return article_url_list


def get_all_titles(articles):
    titles = []
    for i in range(len(articles)):
        page = requests.get(articles[i])
        soup = BeautifulSoup(page.text, 'html.parser')
        title_list = soup.find('h1', class_ ='print-only')
        titles.append(title_list.string)

    return titles


def get_all_datetime(articles):

    datetime_list = []

    for i in range(len(articles)):
        page = requests.get(articles[i])
        soup = BeautifulSoup(page.text, 'html.parser')
        date_temp = soup.find('p', class_ = 'dateline print-only')
        date_temp_text = date_temp.get_text()
        date_temp_text_final = date_temp_text[11:33]
        date_temp_text_final.strip()
        datetime_list.append(date_temp_text_final)

    return datetime_list


def get_primary_contents(articles):

    primary_contents = []

    for i in range(len(articles)):
        page = requests.get(articles[i])
        soup = BeautifulSoup(page.text, 'html.parser')
        bold_content = soup.find("meta",  property="og:description")
        primary_contents.append(bold_content.get("content"))

    return primary_contents


def get_full_article_data(articles, primary_contents):

    list_article = []

    for i in range(len(articles)):
        page = requests.get(articles[i])
        soup = BeautifulSoup(page.text, 'html.parser')

        article_body = soup.find('div', class_ = 'custombody print-only')
        x = article_body.find_all('p')
        article = ''
        final_article = ''
        list_paragraphs = []

        for j in range(len(x)):
            temp = x[j].text.strip()
            temp = temp.replace('\n', ' ')
            list_paragraphs.append(temp)

        article = "".join(list_paragraphs)

        final_article = primary_contents[i] + "\n" + article
        list_article.append(final_article)

    return list_article


def get_json_file(articles, titles, datetime_list, list_article):

    basic_path = os.path.dirname(__file__)

    for i in range(len(articles)):
        json_file = {'title': titles[i], 'date': datetime_list[i], 'content': list_article[i]}
        date_local_directory = datetime_list[i].strip()
        hashed_url = compute_MD5_hash(articles[i]).upper()

        local_directory_format = hashed_url + '.json'

        directory_temp_date = datetime_list[i].lstrip()
        directory_temp_date = directory_temp_date[0:11]
        directory_temp_date = directory_temp_date.replace(' ', '-')

        new_path = r'bdnews24.bangla'
        new_path = new_path + "\\" + directory_temp_date

        file_path = basic_path + "\\" + new_path

        if not os.path.exists(file_path):
            os.makedirs(file_path, mode=0o777)

        file_path_name = file_path + "\\" + local_directory_format

        with open(file_path_name, 'w', encoding='utf-8') as f:
            json.dump(json_file, f, ensure_ascii=False)


request_url = 'https://bangla.bdnews24.com/'
soup = get_soup(request_url)
article_url_list = get_all_news_url(soup)
titles = get_all_titles(article_url_list)
datetime_list = get_all_datetime(article_url_list)
primary_contents = get_primary_contents(article_url_list)
list_article = get_full_article_data(article_url_list, primary_contents)
get_json_file(article_url_list, titles, datetime_list, list_article)
