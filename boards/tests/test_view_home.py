import django
from django.urls import resolve
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from ..views import home, board_topics, new_topic
from ..models import Board, Topic, Post
from ..forms import NewTopicForm


class HomeTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        django.setup()

    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        url = reverse('boards:home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEqual(self.response.status_code, 200) # 测试首页成功返回

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home) # 测试首页调用正确的视图函数

    def test_home_view_contains_link_to_topics_page(self):
        # 测试首页包含指向各个版块的链接
        board_topics_url = reverse('boards:topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))