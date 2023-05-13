from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlparse, urlencode
import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import tldextract
# from .models import Article, Category

# # if request.method == 'POST':
# #     # URL of the news article to scrape
# #     url = request.POST.get('url')
# url = 'https://www.theguardian.com'
# # domain_name = urlparse(url).netloc.split('.')[1]
# domain_name = tldextract.extract(url).domain
#
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')
#
# if domain_name == 'rte':
#     maincontent_div = soup.find('div', {'id': 'primary-nav-global'})
#     cat_params = ['news', 'sport', 'entertainment', 'business', 'lifestyle', 'culture']
# elif domain_name == 'theguardian':
#     maincontent_div = soup.find('ul', {'class': 'pillars'})
#     cat_params = ['international', 'commentisfree', 'sport', 'culture',
#                   'lifeandstyle']  # The guardian cat_params aren't needed but the rte ones are
#
# links = maincontent_div.find_all('a')
# urls = []
# for link in links:
#     href = link.get('href')
#     full_url = urljoin(url, href)
#     if full_url not in urls and any(cat in href.lower() for cat in cat_params):
#         urls.append(full_url)
#
# for url in urls:
#     print(url)

# maincontent_div = soup.find('div', {'data-id': 'uk/commentisfree/regular-stories'}) # Opinion


# if domain_name == 'rte':
#     maincontent_div = soup.find('div', {'id': 'maincontent'})
# elif domain_name == 'theguardian':
#     maincontent_div = soup.find('div', {'data-title': 'Headlines'}) # News
#     maincontent_div = soup.find('div', {'data-title': 'Sport'}) # Sport
#     maincontent_div = soup.find('div', {'data-title': 'Culture'}) # Culture
#     maincontent_div = soup.find('div', {'data-title': 'Lifestyle'}) # Lifestyle
#     maincontent_div = soup.find('div', {'data-title': 'Opinion'}) # Opinion

# Make a GET request to the URL and store the response
# url = 'https://www.theguardian.com/international' # News - works
# url = 'https://www.theguardian.com/uk/commentisfree' # Opinion
# url = 'https://www.theguardian.com/uk/sport' # Sport
# url = 'https://www.theguardian.com/uk/culture' # Culture
# url = 'https://www.theguardian.com/uk/lifeandstyle' # Lifestyle
# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.urls import reverse
# from urllib.parse import urlparse, urlencode
# import requests
# from django.shortcuts import render
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# import tldextract
# # from .models import Article, Category
#
# # # if request.method == 'POST':
# # #     # URL of the news article to scrape
# # #     url = request.POST.get('url')
# # url = 'https://www.theguardian.com'
# # # domain_name = urlparse(url).netloc.split('.')[1]
# # domain_name = tldextract.extract(url).domain
# #
# # response = requests.get(url)
# # soup = BeautifulSoup(response.text, 'html.parser')
# #
# # if domain_name == 'rte':
# #     maincontent_div = soup.find('div', {'id': 'primary-nav-global'})
# #     cat_params = ['news', 'sport', 'entertainment', 'business', 'lifestyle', 'culture']
# # elif domain_name == 'theguardian':
# #     maincontent_div = soup.find('ul', {'class': 'pillars'})
# #     cat_params = ['international', 'commentisfree', 'sport', 'culture',
# #                   'lifeandstyle']  # The guardian cat_params aren't needed but the rte ones are
# #
# # links = maincontent_div.find_all('a')
# # urls = []
# # for link in links:
# #     href = link.get('href')
# #     full_url = urljoin(url, href)
# #     if full_url not in urls and any(cat in href.lower() for cat in cat_params):
# #         urls.append(full_url)
# #
# # for url in urls:
# #     print(url)
#
# # maincontent_div = soup.find('div', {'data-id': 'uk/commentisfree/regular-stories'}) # Opinion
#
#
# # if domain_name == 'rte':
# #     maincontent_div = soup.find('div', {'id': 'maincontent'})
# # elif domain_name == 'theguardian':
# #     maincontent_div = soup.find('div', {'data-title': 'Headlines'}) # News
# #     maincontent_div = soup.find('div', {'data-title': 'Sport'}) # Sport
# #     maincontent_div = soup.find('div', {'data-title': 'Culture'}) # Culture
# #     maincontent_div = soup.find('div', {'data-title': 'Lifestyle'}) # Lifestyle
# #     maincontent_div = soup.find('div', {'data-title': 'Opinion'}) # Opinion
#
# # Make a GET request to the URL and store the response
# # url = 'https://www.theguardian.com/international' # News - works
# # url = 'https://www.theguardian.com/uk/commentisfree' # Opinion
# # url = 'https://www.theguardian.com/uk/sport' # Sport
# # url = 'https://www.theguardian.com/uk/culture' # Culture
# # url = 'https://www.theguardian.com/uk/lifeandstyle' # Lifestyle
#
# response = requests.get(url)
# domain_name = 'theguardian'
#
# # Parse the HTML content of the response with BeautifulSoup
# soup = BeautifulSoup(response.content, 'html.parser')
#
# # Extract the article title
# maincontent_div = None
# if domain_name == 'rte':
#     maincontent_div = soup.find('div', {'id': 'maincontent'})
# elif domain_name == 'theguardian':
#     data_titles = ['Headlines', 'Sport', 'Culture', 'Lifestyle', 'Opinion']
#     for title in data_titles:
#         maincontent_div = soup.find('div', {'data-title': title})
#         if maincontent_div:
#             break
#
# # Gather the list of articles for the given category
# links = maincontent_div.find_all('a')
# urls = []
# for link in links:
#     href = link.get('href')
#     full_url = urljoin(url, href)
#     if full_url not in urls:
#         urls.append(full_url)
#
# for url in urls[:4]:
#     # Make a GET request to the URL and store the response
#     print(url)