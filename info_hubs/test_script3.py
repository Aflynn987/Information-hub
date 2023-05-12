import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlparse, urlencode
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urljoin

""" This gets the articles from the Guardian category page"""
### Scrape Category - Guardian

url = 'https://www.theguardian.com/international'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


# The main difference is here, which div we are specifying when making changes
maincontent_div = soup.find('div', {'data-title': 'Headlines'})

if maincontent_div:
    links = maincontent_div.find_all('a')
    urls = []
    for link in links:
        href = link.get('href')
        # if '/news/business/' in href:
        full_url = urljoin(url, href)
        if full_url not in urls:
            urls.append(full_url)
    print(urls)
