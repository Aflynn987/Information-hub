import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlparse, urlencode
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
from urllib.parse import urljoin

""" This gets the articles from the Guardian category page"""
### Scrape Category - Guardian

# url = 'https://www.theguardian.com/international' # News - works - works
url = 'https://www.theguardian.com/uk/commentisfree' # Opinion - sometimes works
# url = 'https://www.theguardian.com/uk/sport' # Sport - works
# url = 'https://www.theguardian.com/uk/culture' # Culture - sometimes works
# url = 'https://www.theguardian.com/uk/lifeandstyle' # Lifestyle - works

# Make a GET request to the URL and store the response
response = requests.get(url)
domain_name = 'theguardian'
# time.sleep(2)  # wait for 2 seconds

# Parse the HTML content of the response with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Extract the article title
maincontent_div = None
if domain_name == 'rte':
    maincontent_div = soup.find('div', {'id': 'maincontent'})
elif domain_name == 'theguardian':
    data_titles = ['Headlines', 'Sport', 'Culture', 'Lifestyle', 'Opinion']
    for title in data_titles:
        maincontent_div = soup.find('div', {'data-title': title})
        if maincontent_div:
            break

# Gather the list of articles for the given category
if maincontent_div:
    links = maincontent_div.find_all('a')
    urls = []
    for link in links:
        href = link.get('href')
        full_url = urljoin(url, href)
        if full_url not in urls:
            urls.append(full_url)

    print(urls[:3])



    # for url in urls[:10]:
    #     # Make a GET request to the URL and store the response
    #     print(url)
else:
    print(f"No div with expected data-title attribute found in {url}")

# urls = [
#     'https://www.theguardian.com/international',
#     'https://www.theguardian.com/uk/commentisfree',
#     'https://www.theguardian.com/uk/sport',
#     'https://www.theguardian.com/uk/culture',
#     'https://www.theguardian.com/uk/lifeandstyle',
# ]
# domain_name = 'theguardian'
# for url in urls:
#     # Make a GET request to the URL and store the response
#     response = requests.get(url)
#
#     # Parse the HTML content of the response with BeautifulSoup
#     soup = BeautifulSoup(response.content, 'html.parser')
#
#     # Extract the article title
#     maincontent_div = None
#     if domain_name == 'rte':
#         maincontent_div = soup.find('div', {'id': 'maincontent'})
#     elif domain_name == 'theguardian':
#         data_titles = ['Headlines', 'Sport', 'Culture', 'Lifestyle', 'Opinion']
#         for title in data_titles:
#             maincontent_div = soup.find('div', {'data-title': title})
#             if maincontent_div:
#                 break
#
#     # Gather the list of articles for the given category
#     links = maincontent_div.find_all('a')
#     urls = []
#     for link in links:
#         href = link.get('href')
#         full_url = urljoin(url, href)
#         if full_url not in urls:
#             urls.append(full_url)
#
#     for url in urls[:2]:
#         # Make a GET request to the URL and store the response
#         print(url)