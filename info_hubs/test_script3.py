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


url = 'https://www.rte.ie/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

maincontent_div = soup.find('div', {'id': 'primary-nav-global'})
cat_params = ['news', 'sport', 'entertainment', 'business', 'lifestyle', 'culture']

if maincontent_div:
    links = maincontent_div.find_all('a')
    urls = []
    for link in links:
        href = link.get('href')
        full_url = urljoin(url, href)
        if full_url not in urls and any(cat in href.lower() for cat in cat_params):
            urls.append(full_url)
    print(urls)