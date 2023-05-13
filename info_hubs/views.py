from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlparse, urlencode
import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import tldextract
from .models import Article, Category


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

        links = maincontent_div.find_all('a')
        urls = []
        for link in links:
            href = link.get('href')
            full_url = urljoin(url, href)
            if full_url not in urls and 'author' not in href:
                if 'cat_params' in locals() and any(cat in href.lower() for cat in cat_params):
                    urls.append(full_url)
                elif 'cat_params' not in locals():
                    urls.append(full_url)

        if domain_name != 'theamericanconservative':
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

    path = urlparse(url).path
    categories = list(Category.objects.order_by('date_added'))
    # Convert category text to lowercase before comparison
    if domain_name == 'theamericanconservative':
        category_text = 'opinion'
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

    # Create an Article object with the category and article text
    article = Article.objects.create(
        category=category,
        text=output_string
    )

    # Save the article instance to the database
    article.save()