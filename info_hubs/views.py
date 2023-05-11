from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlparse, urlencode
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .models import Article, Category

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
        url = request.POST.get('url')

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

            for url in urls:
                scrape_category(url)

        # Return a success message
        return redirect(reverse('info_hubs:scrape_data') + '?' + urlencode({'success': 'true'}))

    else:
        success = request.GET.get('success')
        context = {'success': success}
        return render(request, 'info_hubs/scrape.html', context=context)

def scrape_category(url):
    # Make a GET request to the URL and store the response
    response = requests.get(url)

    # Parse the HTML content of the response with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the article title
    maincontent_div = soup.find('div', {'id': 'maincontent'})

    # Gather the list of articles for the given category
    if maincontent_div:
        links = maincontent_div.find_all('a')
        urls = []
        for link in links:
            href = link.get('href')
            # if '/news/business/' in href:
            full_url = urljoin(url, href)
            if full_url not in urls:
                urls.append(full_url)

        for url in urls[:4]:
            # Make a GET request to the URL and store the response
            scrape_article(url)
def scrape_article(url):
    # Make a GET request to the URL and store the response
    response = requests.get(url)

    # Parse the HTML content of the response with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the article title
    title = soup.find('h1', class_='headline').text.strip()

    # Extract the article image URL (if one exists)
    image = soup.find('div', class_='article_image')
    if image:
        image_url = image.find('img')['src']
        image_tag = f'<a href="{image_url}"><img src="{image_url}" /></a>'
    else:
        image_tag = ''

    # Extract the article text and limit to 100 characters
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

    # Construct the output string
    output_string = f'<h3>{title}</h3> {image_tag} <p> {article_text}... </p> <br> <p> Link: {link} </p> <p> Author: {author} </p> <p> Site: {site} </p>'

    # Parse the category from the url
    path = urlparse(url).path
    categories = list(Category.objects.order_by('date_added'))
    # Convert category text to lowercase before comparison
    category = next((cat for cat in categories if cat.text.lower() in path and cat.text.lower() != 'news'),
                    None)
    # If a Category object does not exist, create one using the actual path
    if not category:
        new_category = path.split('/')[2]  # Extract the third part of the path as the category
        category = Category.objects.create(text=new_category)

    # Create an Article object with the category and article text
    article = Article.objects.create(
        category=category,
        text=output_string
    )

    # Save the article instance to the database
    article.save()