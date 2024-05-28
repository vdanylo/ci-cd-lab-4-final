from django.contrib.auth.models import User
from django.test import TestCase
from core.forms import LoginForm, SignupForm
from django.test import RequestFactory


class TestForms(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            password='TesT1234$#@!'
        )

    def test_login_form(self):
        request = self.factory.get('/login')
        form = LoginForm(request, data={
            'username': 'testuser',
            'password': 'TesT1234$#@!'
        })
        self.assertTrue(form.is_valid())

    def test_signup_form(self):
        form_data = {
            'username': 'testuser_2',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
        form = SignupForm(data=form_data)
        self.assertTrue(form.is_valid())
