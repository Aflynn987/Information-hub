from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


class TestAuthViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.link = "http://ec2-13-50-14-60.eu-north-1.compute.amazonaws.com:3000"

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get((self.link+'/users/logout/'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_register_view_get(self):
        response = self.client.get((self.link+'/users/register/'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertContains(response, '<a href="/users/register/">Register</a>')
        self.assertContains(response, '<button name="submit">register</button>')

    def test_register_view_post_valid(self):
        form_data = {
            'username': 'newuser',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post((self.link+'/users/register/'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        user = authenticate(username='newuser', password='newpass123')
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'newuser')

    def test_register_view_post_invalid(self):
        form_data = {
            'username': 'testuser',
            'password1': 'testpass',
            'password2': 'testpass'
        }
        response = self.client.post((self.link+'/users/register/'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')