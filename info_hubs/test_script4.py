from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlparse, urlencode
import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
# from .models import Article, Category
#
# # # URL of the news article to scrape
# # url = 'https://www.theguardian.com/football/2023/may/11/vincent-kompany-lets-not-put-a-ceiling-on-how-high-we-can-go'
# # urls = [
# # 'https://www.theguardian.com/us-news/2023/may/11/us-mexico-border-title-42-migrant-restrictions-lifting',
# # 'https://www.theguardian.com/us-news/2023/may/11/what-is-title-42-explainer-immigration',
# # 'https://www.theguardian.com/science/2023/may/12/astronomers-capture-largest-cosmic-explosion-ever-witnessed',
# # 'https://www.theguardian.com/world/2023/may/12/hong-kong-political-cartoonist-axed-after-40-years-following-criticism-from-officials',
# # 'https://www.theguardian.com/uk-news/2023/may/12/unionists-angry-as-joe-biden-says-he-visited-northern-ireland-to-make-sure-the-brits-didnt-screw-around',
# # 'https://www.theguardian.com/media/2023/may/11/cnn-chris-licht-trump-town-hall',
# # 'https://www.theguardian.com/world/2023/may/11/muharrem-ince-turkish-presidential-candidate-withdraws-alleged-sex-tape',
# # 'https://www.theguardian.com/us-news/2023/may/11/george-santos-agreement-brazil',
# # 'https://www.theguardian.com/world/2023/may/12/png-minister-apologises-for-calling-daughters-coronation-critics-primitive-animals',
# # 'https://www.theguardian.com/music/2023/may/12/sorry-swifties-bts-revealed-as-authors-of-mystery-book-that-intrigued-the-internet',
# # 'https://www.theguardian.com/australia-news/2023/may/12/banana-appeal-australias-first-genetically-modified-fruit-sent-for-approval'
# # ]
# # """ The above is for news"""
# # urls = [
# #     'https://www.theguardian.com/commentisfree/2023/may/11/republican-protest-britain-police-public-order-act',
# #     'https://www.theguardian.com/commentisfree/2023/may/11/railway-nationalisation-transpennine-express-conservatives',
# #     'https://www.theguardian.com/commentisfree/2023/may/11/turkey-elections-recep-tayyip-erdogan'
# # ]
# # """ The above is for Opinion """
# #
# # Make a GET request to the URL and store the response
# # urls = [
# #     'https://www.theamericanconservative.com/flesh-of-my-flesh-eating-flesh/',
# #     'https://www.theamericanconservative.com/inescapable-ritual/',
# #     'https://www.theamericanconservative.com/the-plot-against-the-court/',
# #     'https://www.theamericanconservative.com/immigration-impotence/',
# #     'https://www.theamericanconservative.com/prosecutors-punt-god-was-framed/',
# #     'https://www.theamericanconservative.com/the-real-victims-of-the-system/',
# #     'https://www.theamericanconservative.com/greek-lessons-from-milley/'
# # ]
# urls = [
#     'https://www.dailykos.com/stories/2023/5/12/2168900/-CNN-s-defense-of-Trump-town-hall-is-generating-more-outrage',
#     'https://www.dailykos.com/stories/2023/5/12/2167150/-Ukraine-Update-The-counteroffensive-hasn-t-begun-but-Russian-panic-is-well-underway',
#     'https://www.dailykos.com/stories/2023/5/12/2168933/-One-very-rich-billionaire-bought-Supreme-Court-and-made-himself-richer',
#     'https://www.dailykos.com/stories/2023/5/12/2169005/-Biden-must-remain-firm-on-not-negotiating-debt-ceiling',
#     'https://www.dailykos.com/stories/2023/5/11/2168817/-CNN-town-hall-was-stark-reminder-of-threat-Trump-poses-to-the-republic',
#     'https://www.dailykos.com/stories/2023/5/12/2168950/-Elon-Musk-hires-new-Twitter-CEO',
#     'https://www.dailykos.com/stories/2023/5/12/2168909/-Santos-admits-to-writing-bad-checks-House-Republicans-don-t-care',
#     'https://www.dailykos.com/stories/2023/5/11/2168588/-Earth-Matters-Shell-oil-makes-another-10-billion-profit-14-000-orphan-oil-wells-need-plugging',
#     'https://www.dailykos.com/stories/2023/5/12/2168948/-Maine-officials-smack-the-hand-of-the-No-Labels-party-those-useful-fools-for-Trump-2024',
#     'https://www.dailykos.com/stories/2023/5/12/2168649/-Cheers-and-Jeers-Rum-and-Coke-FRIDAY',
#     'https://www.dailykos.com/stories/2023/5/12/2168848/-Cartoon-COVID-s-over-party-supplies',
# ]
#
#
# for url in urls:
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
#                       ' AppleWebKit/537.36 (KHTML, like Gecko)'
#                       ' Chrome/58.0.3029.110 Safari/537.36'
#     }
#     response = requests.get(url, headers=headers)
#     # Parse the HTML content of the response with BeautifulSoup
#     soup = BeautifulSoup(response.content, 'html.parser')
#     domain_name = 'dailykos'
#
#     title = 'N/a'
#     if domain_name == 'rte':
#         # Extract the article title
#         title = soup.find('h1', class_='headline').text.strip()
#         # Extract the article image URL (if one exists)
#         image = soup.find('div', class_='article_image')
#         if image:
#             image_url = image.find('img')['src']
#             image_tag = f'<a href="{image_url}"><img src="{image_url}" /></a>'
#         else:
#             image_tag = ''
#         # Extract the article text and limit to 200 characters
#         article_body = soup.find('section', class_='medium-10 medium-offset-1 columns article-body')
#         if article_body:
#             article_text = article_body.find_all('p')[0].text.strip()[:200]
#         else:
#             article_text = 'N/a'
#
#         # Extract the article link, author, and site
#         link = f'<a href="{url}">{url}</a>'
#         author_element = soup.find('span', itemprop='name')
#         author = author_element.text.strip() if author_element else 'N/a'
#         site = 'RTE'
#
#     elif domain_name == 'theguardian':
#         # Extract the article title
#         # title = soup.find('div', {'data-gu-name': 'headline'}).find('h1').text.strip()
#         headline_div = soup.find('div', {'data-gu-name': 'headline'})
#         if headline_div:
#             title_element = headline_div.find('h1')
#             if title_element:
#                 title = headline_div.find('h1').text.strip()
#
#         # Extract the article image URL (if one exists)
#         image = soup.find('div', class_='article_image')
#         if image:
#             image_url = image.find('img')['src']
#             image_tag = f'<a href="{image_url}"><img src="{image_url}" /></a>'
#         else:
#             image_tag = ''
#         # Extract the article text and limit to 100 characters
#         article_body = soup.find('div', {'data-gu-name': 'body'})
#         if article_body:
#             article_text = article_body.find_all('p')[0].text.strip()[:200]
#         else:
#             article_text = 'N/a'
#
#         # Extract the article link, author, and site
#         link = f'<a href="{url}">{url}</a>'
#         author_element = soup.find('a', {'rel': 'author'})
#         author = author_element.text.strip() if author_element else 'N/a'
#         site = 'The Guardian'
#
#     elif domain_name == 'theamericanconservative':
#         # Extract the article title
#         title = soup.find('h2', class_='c-hero-article__title s-medium').text.strip()
#         # title = soup.find('title').text.strip()
#
#
#         # Extract the article image URL (if one exists)
#         image = soup.find('div', class_='article_image')
#         if image:
#             image_url = image.find('img')['src']
#             image_tag = f'<a href="{image_url}"><img src="{image_url}" /></a>'
#         else:
#             image_tag = ''
#         # Extract the article text and limit to 100 characters
#         article_body = soup.find('section', {'class': 'c-blog-post__body'})
#         if article_body:
#             article_text = article_body.find_all('p')[0].text.strip()[:200]
#         else:
#             article_text = 'N/a'
#
#         # Extract the article link, author, and site
#         link = f'<a href="{url}">{url}</a>'
#         author_element = soup.find('a', {'class': 'o-byline__author'})
#         author = author_element.text.strip() if author_element else 'N/a'
#         site = 'The American Conservative'
#
#     elif domain_name == 'dailykos':
#         # Extract the article title
#         title = soup.find('div', class_='story-title').text.strip()
#         # title = soup.find('title').text.strip()
#
#
#         # Extract the article image URL (if one exists)
#         image = soup.find('div', class_='article_image')
#         if image:
#             image_url = image.find('img')['src']
#             image_tag = f'<a href="{image_url}"><img src="{image_url}" /></a>'
#         else:
#             image_tag = ''
#         # Extract the article text and limit to 200 characters
#         article_body = soup.find('div', class_='story-column')
#         if article_body:
#             article_text = article_body.find_all('p')[0].text.strip()[:200]
#         else:
#             article_text = 'N/a'
#
#         # Extract the article link, author, and site
#         link = f'<a href="{url}">{url}</a>'
#         # author_element = soup.find('span', class_='author-name')
#         author_element = soup.find('div', class_='author-byline')
#         author_str = author_element.text.strip() if author_element else 'N/a'
#         # Clean author variable
#         pattern = re.compile(r"\b(for|Daily|kos)\b", flags=re.IGNORECASE)
#         author = re.sub(pattern, "", str(author_str)).strip()
#         site = 'The Daily Kos'
#
#     # Construct the output string
#     output_string = f'<h3>{title}</h3> {image_tag} <p> {article_text}... </p> <br> <p> Link: {link} </p> <p> Author: {author} </p> <p> Site: {site} </p>'
#     # output_string = f"{title}"
#
#     # A dictionary to map terms to categories
#     category_mapping = {
#         'us-news': 'News',
#         'world': 'News',
#         'football': 'Sport',
#         'lifeandstyle': 'Culture',
#         'commentisfree': 'Opinion',
#         'film': 'Entertainment',
#         'tv-and-radio': 'Entertainment',
#         'music': 'Culture',
#         'science': 'Science',
#         'christian-aid-today': 'Opinion',
#     }
#
#
#     path = urlparse(url).path
#     categories = ['Opinion', 'Business', 'Science']
#     # Convert category text to lowercase before comparison
#     category_text = next((cat for cat in categories if cat.lower() in path and cat.lower() != 'news'),
#                     None)
#
#     # Check if a category with the same name already exists
#     existing_category = None
#     if category_text:
#         existing_category = next((cat for cat in categories if cat.lower() == category_text), None)
#
#     # If a Category object does not exist, create one using the actual path
#     if not existing_category:
#         path_parts = path.split('/')
#         new_category = path_parts[1]  # Extract the third part of the path as the category
#         if new_category in category_mapping:
#             category_text = category_mapping[new_category]
#         else:
#             category_text = new_category
#
#
#     else:
#         # Use the existing category object
#         category = existing_category
#
#     # Create an Article object with the category and article text
#     print(category, output_string+"")
#
#     # Save the article instance to the database

urls = [
    'https://www.dailykos.com/stories/2023/5/12/2168900/-CNN-s-defense-of-Trump-town-hall-is-generating-more-outrage',
    'https://www.dailykos.com/stories/2023/5/12/2167150/-Ukraine-Update-The-counteroffensive-hasn-t-begun-but-Russian-panic-is-well-underway',
    'https://www.dailykos.com/stories/2023/5/12/2168933/-One-very-rich-billionaire-bought-Supreme-Court-and-made-himself-richer',
    'https://www.dailykos.com/stories/2023/5/12/2169005/-Biden-must-remain-firm-on-not-negotiating-debt-ceiling',
    'https://www.dailykos.com/stories/2023/5/11/2168817/-CNN-town-hall-was-stark-reminder-of-threat-Trump-poses-to-the-republic',
    'https://www.dailykos.com/stories/2023/5/12/2168950/-Elon-Musk-hires-new-Twitter-CEO',
    'https://www.dailykos.com/stories/2023/5/12/2168909/-Santos-admits-to-writing-bad-checks-House-Republicans-don-t-care',
    'https://www.dailykos.com/stories/2023/5/11/2168588/-Earth-Matters-Shell-oil-makes-another-10-billion-profit-14-000-orphan-oil-wells-need-plugging',
    'https://www.dailykos.com/stories/2023/5/12/2168948/-Maine-officials-smack-the-hand-of-the-No-Labels-party-those-useful-fools-for-Trump-2024',
    'https://www.dailykos.com/stories/2023/5/12/2168649/-Cheers-and-Jeers-Rum-and-Coke-FRIDAY',
    'https://www.dailykos.com/stories/2023/5/12/2168848/-Cartoon-COVID-s-over-party-supplies',
]


for url in urls:
    headers = {

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/58.0.3029.110 Safari/537.36'
    }
# Make a GET request to the URL and store the response
response = requests.get(url, headers=headers)
# Parse the HTML content of the response with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')
domain_name = 'dailykos'
title = 'N/a'
if domain_name == 'rte':
    # Extract the article title
    title = soup.find('h1', class_='headline').text.strip()
    # Extract the article image URL (if one exists)
    image = soup.find('div', class_='article_image')
    if image:
        image_url = image.find('img')['src']
        image_tag = f'<a href="{image_url}"><img src="{image_url}" /></a>'
    else:
        image_tag = ''
    # Extract the article text and limit to 200 characters
    article_body = soup.find('section', class_='medium-10 medium-offset-1 columns article-body')
    if article_body:
        article_text = article_body.find_all('p')[0].text.strip()[:200]
    else:
        article_text = 'N/a'

    # Extract the article link, author, and site
    link = f'<a href="{url}">{url}</a>'
    author_element = soup.find('span', itemprop='name')
    author = author_element.text.strip() if author_element else 'N/a'
    site = 'RTE'

elif domain_name == 'theguardian':
    # Extract the article title
    # title = soup.find('div', {'data-gu-name': 'headline'}).find('h1').text.strip()
    headline_div = soup.find('div', {'data-gu-name': 'headline'})
    if headline_div:
        title_element = headline_div.find('h1')
        if title_element:
            title = headline_div.find('h1').text.strip()

    # Extract the article image URL (if one exists)
    image = soup.find('div', class_='article_image')
    if image:
        image_url = image.find('img')['src']
        image_tag = f'<a href="{image_url}"><img src="{image_url}" /></a>'
    else:
        image_tag = ''
    # Extract the article text and limit to 100 characters
    article_body = soup.find('div', {'data-gu-name': 'body'})
    if article_body:
        article_text = article_body.find_all('p')[0].text.strip()[:200]
    else:
        article_text = 'N/a'

    # Extract the article link, author, and site
    link = f'<a href="{url}">{url}</a>'
    author_element = soup.find('a', {'rel': 'author'})
    author = author_element.text.strip() if author_element else 'N/a'
    site = 'The Guardian'

elif domain_name == 'theamericanconservative':
    # Extract the article title
    title = soup.find('h2', class_='c-hero-article__title s-medium').text.strip()
    # title = soup.find('title').text.strip()

    # Extract the article image URL (if one exists)
    image = soup.find('div', class_='article_image')
    if image:
        image_url = image.find('img')['src']
        image_tag = f'<a href="{image_url}"><img src="{image_url}" /></a>'
    else:
        image_tag = ''
    # Extract the article text and limit to 100 characters
    article_body = soup.find('section', {'class': 'c-blog-post__body'})
    if article_body:
        article_text = article_body.find_all('p')[0].text.strip()[:200]
    else:
        article_text = 'N/a'

    # Extract the article link, author, and site
    link = f'<a href="{url}">{url}</a>'
    author_element = soup.find('a', {'class': 'o-byline__author'})
    author = author_element.text.strip() if author_element else 'N/a'
    site = 'The American Conservative'

elif domain_name == 'dailykos':
    # Extract the article title
    title = soup.find('div', class_='story-title').text.strip()
    # title = soup.find('title').text.strip()

    # Extract the article image URL (if one exists)
    image = soup.find('div', class_='article_image')
    if image:
        image_url = image.find('img')['src']
        image_tag = f'<a href="{image_url}"><img src="{image_url}" /></a>'
    else:
        image_tag = ''
    # Extract the article text and limit to 200 characters
    article_body = soup.find('div', class_='story-column')
    if article_body:
        article_text = article_body.find_all('p')[0].text.strip()[:200]
    else:
        article_text = 'N/a'

    # Extract the article link, author, and site
    link = f'<a href="{url}">{url}</a>'
    # author_element = soup.find('span', class_='author-name')
    author_element = soup.find('div', class_='author-byline')
    author_str = author_element.text.strip() if author_element else 'N/a'
    # Clean author variable
    pattern = re.compile(r"\b(for|Daily|kos)\b", flags=re.IGNORECASE)
    author = re.sub(pattern, "", str(author_str)).strip()
    site = 'The Daily Kos'

# Construct the output string
output_string = f'<h3>{title}</h3> {image_tag} <p> {article_text}... </p> <br> <p> Link: {link} </p> <p> Author: {author} </p> <p> Site: {site} </p>'

# A dictionary to map terms to categories
category_mapping = {
    'us-news': 'News',
    'world': 'News',
    'football': 'Sport',
    'lifeandstyle': 'Culture',
    'commentisfree': 'Opinion',
    'film': 'Entertainment',
    'tv-and-radio': 'Entertainment',
    'music': 'Culture',
    'science': 'Science',
    'christian-aid-today': 'Opinion',
}

category = 'Opinion' if domain_name == 'theamericanconservative' else None
path = urlparse(url).path
categories = ['Opinion', 'Business', 'Science']
# Convert category text to lowercase before comparison
category_text = next((cat for cat in categories if cat.lower() in path and cat.lower() != 'news'),
                     None)

# Check if a category with the same name already exists
existing_category = None
if category_text:
    existing_category = next((cat for cat in categories if cat.lower() == category_text), None)

# If a Category object does not exist, create one using the actual path
if not existing_category:
    path_parts = path.split('/')
    new_category = path_parts[1]  # Extract the third part of the path as the category
    if new_category in category_mapping:
        category_text = category_mapping[new_category]
    else:
        category_text = new_category


else:
    # Use the existing category object
    category = existing_category

# Create an Article object with the category and article text
print(category, output_string + "")

# Save the article instance to the database