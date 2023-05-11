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


url = 'https://www.rte.ie/news/business/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

maincontent_div = soup.find('div', {'id': 'maincontent'})

if maincontent_div:
    links = maincontent_div.find_all('a')
    urls = []
    for link in links:
        href = link.get('href')
        if '/news/business/' in href:
            full_url = urljoin(url, href)
            if full_url not in urls:
                urls.append(full_url)

    for url in urls:

        # Parse the category from the url
        path = urlparse(url).path

        new_category = path.split('/')[2]  # Extract the third part of the path as the category
        print(new_category)