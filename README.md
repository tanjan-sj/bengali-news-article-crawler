# bengali-news-article-crawler
A small scale crawler for scraping Bengali news article from a few select website.

How to run:

1. Clone the repository or download the zip file
2. Run the .py file with any python IDE or on a local machine

**warning: running this project will cause multiple files to download on your local machine**

Features:

1. This project can parse the title, date, and article content of all news articles in the https://bangla.bdnews24.com website.
2. Creates a json dump for the title, date, and article content and saves them to the local machine
3. It encodes the URL of the news article using MD5 hashing, and renames the json dump before saving them

Libraries used:

Python3 with requests, beautifulsoup, hashlib, and json
