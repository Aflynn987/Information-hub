# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.urls import reverse
# from urllib.parse import urlparse, urlencode
# import requests
# from django.shortcuts import render
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# # from .models import Article, Category
#
# # URL of the news article to scrape
# url = 'https://www.theguardian.com/football/2023/may/11/vincent-kompany-lets-not-put-a-ceiling-on-how-high-we-can-go'
# urls = [
# 'https://www.theguardian.com/us-news/2023/may/11/us-mexico-border-title-42-migrant-restrictions-lifting',
# 'https://www.theguardian.com/us-news/2023/may/11/what-is-title-42-explainer-immigration',
# 'https://www.theguardian.com/science/2023/may/12/astronomers-capture-largest-cosmic-explosion-ever-witnessed',
# 'https://www.theguardian.com/world/2023/may/12/hong-kong-political-cartoonist-axed-after-40-years-following-criticism-from-officials',
# 'https://www.theguardian.com/uk-news/2023/may/12/unionists-angry-as-joe-biden-says-he-visited-northern-ireland-to-make-sure-the-brits-didnt-screw-around',
# 'https://www.theguardian.com/media/2023/may/11/cnn-chris-licht-trump-town-hall',
# 'https://www.theguardian.com/world/2023/may/11/muharrem-ince-turkish-presidential-candidate-withdraws-alleged-sex-tape',
# 'https://www.theguardian.com/us-news/2023/may/11/george-santos-agreement-brazil',
# 'https://www.theguardian.com/world/2023/may/12/png-minister-apologises-for-calling-daughters-coronation-critics-primitive-animals',
# 'https://www.theguardian.com/music/2023/may/12/sorry-swifties-bts-revealed-as-authors-of-mystery-book-that-intrigued-the-internet',
# 'https://www.theguardian.com/australia-news/2023/may/12/banana-appeal-australias-first-genetically-modified-fruit-sent-for-approval'
# ]
# """ The above is for news"""
# urls = [
#     'https://www.theguardian.com/commentisfree/2023/may/11/republican-protest-britain-police-public-order-act',
#     'https://www.theguardian.com/commentisfree/2023/may/11/railway-nationalisation-transpennine-express-conservatives',
#     'https://www.theguardian.com/commentisfree/2023/may/11/turkey-elections-recep-tayyip-erdogan'
# ]
# """ The above is for Opinion """
#
# # Make a GET request to the URL and store the response
# for url in urls:
#     response = requests.get(url)
#
#     # Parse the HTML content of the response with BeautifulSoup
#     soup = BeautifulSoup(response.content, 'html.parser')
#
#     # Extract the article title
#     # title = soup.find('h1', class_='headline').text.strip()
#     # title = soup.find('h1', {'data-gu-name': 'headline'}).text.strip()
#     title = soup.find('div', {'data-gu-name': 'headline'}).find('h1').text.strip()
#     """ TODO: The above is likely incorrect but we will see after more work"""
#
#
#     # Extract the article image URL (if one exists)
#     image = soup.find('div', class_='article_image')
#     """ TODO: Above is also likely incorrect"""
#
#     if image:
#         image_url = image.find('img')['src']
#         image_tag = f'<a href="{image_url}"><img src="{image_url}" /></a>'
#     else:
#         image_tag = ''
#
#     # Extract the article text and limit to 100 characters
#     # article_body = soup.find('section', class_='medium-10 medium-offset-1 columns article-body')
#     #     article_body = soup.find('div', {'data-gu-name': 'body'}).text.strip()
#     #
#     #     if article_body:
#     #         article_text = article_body.find_all('p')[0].text.strip()[:200]
#     #     else:
#     #         article_text = 'N/a'
#     article_body = soup.find('div', {'data-gu-name': 'body'})
#
#     if article_body:
#         article_text = article_body.find_all('p')[0].text.strip()[:200]
#     else:
#         article_text = 'N/a'
#
#     # Extract the article link, author, and site
#     link = f'<a href="{url}">{url}</a>'
#     author_element = soup.find('a', {'rel': 'author'})
#     # author_element = soup.find('span', itemprop='name')
#     author = author_element.text.strip() if author_element else 'N/a'
#     site = 'The Guardian'
#
#     # Construct the output string
#     output_string = f'<h3>{title}</h3> {image_tag} <p> {article_text}... </p> <br> <p> Link: {link} </p> <p> Author: {author} </p> <p> Site: {site} </p>'
#
#     print(output_string)
#
#
# # # Parse the category from the url
# # path = urlparse(url).path
# # categories = list(Category.objects.order_by('date_added'))
# # # Convert category text to lowercase before comparison
# # category = next((cat for cat in categories if cat.text.lower() in path and cat.text.lower() != 'news'),
# #                 None)
# # # If a Category object does not exist, create one using the actual path
# # if not category:
# #     new_category = path.split('/')[1]  # Extract the third part of the path as the category
# #     category = Category.objects.create(text=new_category)
# #
# # # Create an Article object with the category and article text
# # article = Article.objects.create(
# #     category=category,
# #     text=output_string
# # )
# #
# # # Save the article instance to the database
# # article.save()