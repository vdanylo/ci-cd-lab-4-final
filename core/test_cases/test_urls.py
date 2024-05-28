from django.test import TestCase, Client
from django.urls import reverse, resolve
from core.views import signup
from django.contrib.auth.views import LoginView, LogoutView


class TestUrls(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup_url(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func, signup)

    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_logout_url(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, LogoutView)
