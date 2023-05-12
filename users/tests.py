from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from unittest.mock import patch

# Create your tests here.

class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('info_hubs:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.user.is_authenticated)

class RegisterTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('users:register')

    def test_register_GET(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_POST_valid_form(self):
        data = {
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='testuser')
        self.assertTrue(user.is_authenticated)

    def test_register_POST_invalid_form(self):
        data = {
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'testpass456',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertFormError(response, 'form', 'password2', 'The two password fields didn’t match.')