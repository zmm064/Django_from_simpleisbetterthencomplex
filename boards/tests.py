import django
from django.core.urlresolvers import reverse
from django.test import TestCase
from .views import home

# TODO: Configure your database in settings.py and sync before running tests.

class HomeTests(TestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        django.setup()

    def test_home_view_status_code(self):
        url = reverse('boards:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)