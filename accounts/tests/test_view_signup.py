"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import django
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.urls import resolve
from django.test import TestCase

from ..forms import SignUpForm
from ..views import signup

# TODO: Configure your database in settings.py and sync before running tests.

class SignUpTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        django.setup()

    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_form_inputs(self):
        '''
        The view must contain and only contain five inputs: 
        csrf, username, email, password1, password2
        '''
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'john',
            'email': 'john@doe.com',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('boards:home')

    def test_redirection(self):
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated())


class InvalidSignUpTests(TestCase):
    # 1.这次我们提交错误的表单数据
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {'error_data':'error_data'})  # submit an empty dictionary

    # 2.在这种情况下页面不会跳转
    def test_signup_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    # 3.返回的页面会包含错误信息
    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    # 4.结果是我们没有成功创建用户
    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())