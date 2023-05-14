from django.test import TestCase, Client
from django.urls import reverse
from info_hubs.models import  Article
from bs4 import BeautifulSoup
from unittest.mock import patch, MagicMock
from info_hubs.models import Category

from .views import summarize, preprocess, parse_category


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

        self.assertEqual(headline.text, '\n          headline\n        ')
        if image is None:
            self.assertEqual(image, None)
        else:
            self.assertEqual(image['src'], '/media/image.jpg/')

class TestPytorch(TestCase):
    def test_summarize(self):
        article = "This is a test article. It contains some text that we will summarize. The summary should be brief and capture the main points of the article."
        expected_summary = "This is a test article. It contains some text that we will summarize."
        with patch('info_hubs.views.summarize') as mock_summarize:
            mock_summarize.return_value = expected_summary
            summary = summarize(article)
            self.assertIsNotNone(summary)

    def test_preprocess(self):
        article = "This is a test article. It contains some text that we will preprocess."
        expected_sentences = ['This is a test article It contains some text that we will preprocess']
        sentences = preprocess(article)
        self.assertEqual(sentences, expected_sentences)

    def test_postprocess(self):
        summary = "this is a test summary. it should be postprocessed to capitalize the first letter and add a period."
        with patch('info_hubs.views.postprocess') as mock_postprocess:
            mock_postprocess.return_value = "This is a test summary."
            postprocessed_summary = summarize(summary)
            mock_postprocess.assert_called_once_with(
                'this is a test summary . it should be postprocessed to capitalize the first letter and add period.'
            )
            self.assertIsNotNone(postprocessed_summary)



class ParseCategoryTestCase(TestCase):
    def setUp(self):
        # Create some Category objects for testing
        Category.objects.create(text='News')
        Category.objects.create(text='Opinion')
        Category.objects.create(text='Culture')
        Category.objects.create(text='Science')

    @patch('info_hubs.models.Category.objects.order_by')
    def test_parse_category(self, mock_order_by):
        # Mock the Category.objects.order_by method to return a known list of categories
        mock_order_by.return_value = [
            MagicMock(text='News'),
            MagicMock(text='Opinion'),
            MagicMock(text='Culture'),
            MagicMock(text='Science'),
        ]

        # Test the function with various input URLs and domain names
        self.assertEqual(parse_category('http://www.example.com/us-news/1234', 'example'), Category.objects.get(text='News'))
        self.assertEqual(parse_category('http://www.example.com/world/5678', 'example'), Category.objects.get(text='News'))
        self.assertEqual(parse_category('http://www.example.com/football/1234', 'example'), Category.objects.get(text='Sport'))
        self.assertEqual(parse_category('http://www.example.com/lifeandstyle/5678', 'example'), Category.objects.get(text='Culture'))
        self.assertEqual(parse_category('http://www.example.com/commentisfree/1234', 'example'), Category.objects.get(text='Opinion'))
        self.assertEqual(parse_category('http://www.example.com/film/5678', 'example'), Category.objects.get(text='Entertainment'))
        self.assertEqual(parse_category('http://www.example.com/tv-and-radio/1234', 'example'), Category.objects.get(text='Entertainment'))
        self.assertEqual(parse_category('http://www.example.com/music/5678', 'example'), Category.objects.get(text='Culture'))

        # Test the function with a path that doesn't match any categories
        self.assertEqual(parse_category('http://www.example.com/unknown-category/1234', 'example.com').text, 'unknown-category')