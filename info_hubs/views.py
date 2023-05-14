from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlparse, urlencode
import requests
import re
from django.shortcuts import render
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import tldextract
from .models import Article, Category

## pytorch imports
import re
import string
import nltk
import torch
from nltk.tokenize import sent_tokenize
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer

from .models import Category


# Create your views here.
def index(request):
    """The home page for information hub"""
    return render(request, 'info_hubs/index.html')


def categories(request):
    """Show all categories"""
    categories = Category.objects.order_by('date_added')
    context = {'categories': categories}
    return render(request, 'info_hubs/categories.html', context)


def category(request, category_id):
    """Show a single category and all its articles"""
    category = Category.objects.get(id=category_id)
    articles = category.article_set.order_by('-date_added')

    for article in articles:
        soup = BeautifulSoup(article.text, 'html.parser')
        headline = soup.find('h3')
        image = soup.find('a href')
        if headline:
            article.headline = headline.text
            article.text = str(soup).replace(str(headline), '')
        if image:
            article.image = image['href']
            article.text = str(soup).replace(str(image), '')

    context = {'category': category, 'articles': articles}
    return render(request, 'info_hubs/category.html', context)


def scrape_data(request):
    if request.method == 'POST':
        # URL of the news article to scrape
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                          ' AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/58.0.3029.110 Safari/537.36'
        }
        url = request.POST.get('url')
        domain_name = tldextract.extract(url).domain

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        if domain_name == 'rte':
            maincontent_div = soup.find('div', {'id': 'primary-nav-global'})
            cat_params = ['news', 'sport', 'entertainment', 'business', 'lifestyle', 'culture']
        elif domain_name == 'theguardian':
            maincontent_div = soup.find('ul', {'class': 'pillars'})
            cat_params = ['international', 'commentisfree', 'sport', 'culture',
                          'lifeandstyle']  # The guardian cat_params aren't needed but the rte ones are
        elif domain_name == 'theamericanconservative':
            maincontent_div = soup.find('div', {'class': 'c-featured-posts__posts'})
        elif domain_name == 'dailykos':
            maincontent_div = [soup.find('div', {'class': 'top-news__primary_news'}),
                               soup.find('div', {'class': 'top-news__secondary_news'}),
                               soup.find('div', {'class': 'top-news__more_news'})]

        links = []
        if isinstance(maincontent_div, list):
            for div in maincontent_div:
                links += div.find_all('a')
        else:
            links = maincontent_div.find_all('a')

        urls = []
        for link in links:
            href = link.get('href')
            full_url = urljoin(url, href)
            if full_url not in urls and 'author' or 'Cartoon' not in href:
                if 'cat_params' in locals() and any(cat in href.lower() for cat in cat_params):
                    urls.append(full_url)
                elif 'cat_params' not in locals():
                    urls.append(full_url)

        if domain_name != 'theamericanconservative' or 'dailykos':
            for url in urls:
                scrape_category(url, domain_name, headers)
        else:
            for url in urls:
                scrape_article(url, domain_name, headers)

        # Return a success message
        return redirect(reverse('info_hubs:scrape_data') + '?' + urlencode({'success': 'true'}))

    else:
        success = request.GET.get('success')
        context = {'success': success}
        return render(request, 'info_hubs/scrape.html', context=context)


def scrape_category(url, domain_name, headers):
    # Make a GET request to the URL and store the response
    response = requests.get(url, headers=headers)

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
                # category = 'News' if title == 'Headlines' else title
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

        for url in urls[:4]:
            domain_name_validation = tldextract.extract(url).domain
            if domain_name != domain_name_validation:
                break
            # Make a GET request to the URL and store the response
            scrape_article(url, domain_name, headers)


def scrape_article(url, domain_name, headers):
    # Make a GET request to the URL and store the response
    response = requests.get(url, headers=headers)
    # Parse the HTML content of the response with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    if domain_name == 'rte':
        output_string = scrape_rte(url, soup)
    elif domain_name == 'theguardian':
        output_string = scrape_guardian(url, soup)
    elif domain_name == 'theamericanconservative':
        output_string = scrape_ac(url, soup)
    elif domain_name == 'dailykos':
        output_string = scrape_kos(url, soup)

    category = parse_category(url, domain_name)

    # Create an Article object with the category and article text
    article = Article.objects.create(
        category=category,
        text=output_string
    )

    # Save the article instance to the database
    article.save()


def scrape_rte(url, soup):
    # Extract the article title
    title_element = soup.find('h1', class_='headline')
    title = title_element.text.strip() if title_element else 'N/a'
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
        article = article_body.find_all('p')[0].text.strip()[:200]
        article_text = summarize(article)
    else:
        article_text = 'N/a'

    # Extract the article link, author, and site
    link = f'<a href="{url}">{url}</a>'
    author_element = soup.find('span', itemprop='name')
    author = author_element.text.strip() if author_element else 'N/a'
    site = 'RTE'
    output_string = f'<h3>{title}</h3> {image_tag} <p> {article_text}... </p> <br> <p> Link: {link} </p> <p> Author: {author} </p> <p> Site: {site} </p>'
    return output_string


def scrape_guardian(url, soup):
    title_element = soup.find('div', {'data-gu-name': 'headline'})
    title = title_element.text.strip() if title_element else 'N/a'

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
        article = article_body.find_all('p')[0].text.strip()[:200]
        article_text = summarize(article)
    else:
        article_text = 'N/a'

    # Extract the article link, author, and site
    link = f'<a href="{url}">{url}</a>'
    author_element = soup.find('a', {'rel': 'author'})
    author = author_element.text.strip() if author_element else 'N/a'
    site = 'The Guardian'
    output_string = f'<h3>{title}</h3> {image_tag} <p> {article_text}... </p> <br> <p> Link: {link} </p> <p> Author: {author} </p> <p> Site: {site} </p>'
    return output_string


def scrape_ac(url, soup):
    # Extract the article title
    title_element = soup.find('h2', class_='c-hero-article__title s-medium')
    title = title_element.text.strip() if title_element else 'N/a'

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
        article = article_body.find_all('p')[0].text.strip()[:200]
        article_text = summarize(article)
    else:
        article_text = 'N/a'

    # Extract the article link, author, and site
    link = f'<a href="{url}">{url}</a>'
    author_element = soup.find('a', {'class': 'o-byline__author'})
    author = author_element.text.strip() if author_element else 'N/a'
    site = 'The American Conservative'
    output_string = f'<h3>{title}</h3> {image_tag} <p> {article_text}... </p> <br> <p> Link: {link} </p> <p> Author: {author} </p> <p> Site: {site} </p>'
    return output_string


def scrape_kos(url, soup):
    # Extract the article title
    title_element = soup.find('div', class_='story-title')
    title = title_element.text.strip() if title_element else 'N/a'

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
        article = article_body.find_all('p')[0].text.strip()[:200]
        article_text = summarize(article)
    else:
        article_text = 'N/a'

    # Extract the article link, author, and site
    link = f'<a href="{url}">{url}</a>'
    # author_element = soup.find('span', class_='author-name')
    author_element = soup.find('div', class_='author-byline')
    author_str = author_element.text.strip() if author_element else 'N/a'
    # Clean author variable
    pattern = re.compile(r"\b(for|Daily|kos)\b", flags=re.IGNORECASE)
    author = re.sub(pattern, "", author_str).strip()
    site = 'The Daily Kos'
    # Construct the output string
    output_string = f'<h3>{title}</h3> {image_tag} <p> {article_text}... </p> <br> <p> Link: {link} </p> <p> Author: {author} </p> <p> Site: {site} </p>'
    return output_string


def parse_category(url, domain_name):
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

    path = urlparse(url).path
    categories = list(Category.objects.order_by('date_added'))
    # Convert category text to lowercase before comparison
    if domain_name == 'theamericanconservative':
        category_text = 'opinion'
    elif domain_name == 'dailykos':
        category_text = 'news'
    else:
        category_text = next((cat for cat in categories if cat.text.lower() in path and cat.text.lower()
                              != 'news'), None)

    # Check if a category with the same name already exists
    existing_category = None
    if category_text:
        existing_category = next((cat for cat in categories if cat.text.lower() == category_text), None)

    # If a Category object does not exist, create one using the actual path
    if not existing_category:
        path_parts = path.split('/')
        new_category = path_parts[1]  # Extract the third part of the path as the category
        if new_category in category_mapping:
            category_text = category_mapping[new_category]
        else:
            category_text = new_category

        # Create a new category object if it doesn't exist yet
        category, created = Category.objects.get_or_create(text=category_text)
    else:
        # Use the existing category object
        category = existing_category

    return category


def preprocess(article):
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    # Remove digits
    text = re.sub(r'\d+', '', text)
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Tokenize sentences
    sentences = sent_tokenize(text)
    # Remove short sentences
    sentences = [s for s in sentences if len(s) > 20]
    return sentences

    # Define postprocessing function


def postprocess(article):
    # Remove leading/trailing whitespace
    summary = summary.strip()
    # Capitalize first letter
    summary = summary[0].upper() + summary[1:]
    # Add period if missing
    if summary[-1] not in ['.', '!', '?']:
        summary += '.'
    return summary


def summarize(article):
    model_name = "sshleifer/distilbart-cnn-12-6"
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    summarizer = pipeline(
        "summarization",
        model=model,
        tokenizer=tokenizer,
        framework="pt",
        device=device,
        max_length=190,
        min_length=100,
        num_beams=4,
        length_penalty=2.0,
        early_stopping=True,
        no_repeat_ngram_size=2,
        num_return_sequences=1,
        top_p=0.92,
        top_k=40,
        temperature=0.8
    )

    # Preprocess text
    sentences = preprocess(text)

    # Generate summaries for each sentence
    summaries = []
    for sentence in sentences:
        summary_text = summarizer(sentence)[0]['summary_text']
        summary = postprocess(summary_text)
        summaries.append(summary)

    # Join summaries into a single text
    summary_text = ' '.join(summaries)

    return summary
