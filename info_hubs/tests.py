from django.test import TestCase, Client
from django.urls import reverse
from info_hubs.models import Category, Article
from bs4 import BeautifulSoup

# Tests for info_hubs models
class CategoryTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(text='Culture')

    def test_category_creation(self):
        self.assertTrue(isinstance(self.category, Category))
        self.assertEqual(str(self.category), 'Culture')

    def test_category_text_max_length(self):
        max_length = self.category._meta.get_field('text').max_length
        self.assertEqual(max_length, 200)

class ArticleTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(text='Culture')
        self.article = Article.objects.create(
            category=self.category,
            text='The Science of Music'
        )

    def test_article_creation(self):
        self.assertTrue(isinstance(self.article, Article))
        self.assertEqual(str(self.article), 'The Science of Music')

    def test_article_text_max_length(self):
        max_length = self.article._meta.get_field('text').max_length
        self.assertEqual(max_length, None)

    def test_article_category_relationship(self):
        self.assertEqual(self.article.category, self.category)

    def test_split_tag(self):
        self.assertEqual(self.article.split('The Science of Music', ' '), ['The', 'Science', 'of', 'Music'])


# Tests for info_hubs views
class InfoHubViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(text='Test Category')

    def test_index_view(self):
        url = reverse('info_hubs:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info_hubs/index.html')

    def test_categories_view(self):
        url = reverse('info_hubs:categories')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info_hubs/categories.html')

    def test_category_view(self):
        article_text = '<p>Article text with <h3>headline</h3> and <a href="image.jpg">image</a>.</p>'
        article = Article.objects.create(category=self.category, text=article_text)

        url = reverse('info_hubs:category', args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info_hubs/category.html')

        soup = BeautifulSoup(response.content, 'html.parser')
        headline = soup.find('h3')
        image = soup.find('img')

        self.assertEqual(headline.text, 'headline\n')
        self.assertEqual(image['src'], '/media/image.jpg/')

# Tests for webscraping view method
class ScrapeDataViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = 'https://www.rte.ie/news/business/2023/0510/1382716-retailers/'
        self.response = self.client.post(reverse('info_hubs:scrape_data'), {'url': self.url})

    def test_post_request_creates_article(self):
        article = Article.objects.get(category__text='business')
        self.assertEqual(article.category.text, 'business')

    def test_post_request_redirects_to_success_page(self):
        self.assertEqual(self.response.status_code, 302)
        self.assertRedirects(self.response, f"{reverse('info_hubs:scrape_data')}?success=true")

    def test_get_request_returns_scrape_template(self):
        response = self.client.get(reverse('info_hubs:scrape_data'))
        self.assertTemplateUsed(response, 'info_hubs/scrape.html')

    def test_get_request_success_param(self):
        response = self.client.get(reverse('info_hubs:scrape_data'), {'success': 'true'})
        self.assertContains(response, 'Scraping complete!')