import django
from boards.views import TopicListView
from django.urls import resolve
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from ..views import home, board_topics, new_topic
from ..models import Board, Topic, Post
from ..forms import NewTopicForm


class BoardTopicsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        django.setup()

    def setUp(self):
        # 测试前准备要用的数据，因为Django的测试机制不会使用当前数据库跑你的测试
        # 运行 Django 测试时会即时创建一个新的数据库
        Board.objects.create(name='Django', description='Django board.')
        self.board_topics_url = reverse('boards:topics', kwargs={'pk': 1})
        self.response = self.client.get(self.board_topics_url)
        self.new_topic_url = reverse('boards:new_topic', kwargs={'pk': 1})
        self.homepage_url = reverse('boards:home')

    def test_board_topics_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200) # 测试话题列表页正确返回

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('boards:topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404) # 对不存在的数据返回404

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve(self.board_topics_url)
        #self.assertEquals(view.func, board_topics) # 测试话题列表页调用正确的视图函数
        self.assertEquals(view.func.view_class, TopicListView)

    def test_board_topics_view_contains_link_back_to_homepage(self):
        # 测试版块页包含指向首页的链接
        homepage_url = reverse('boards:home')
        self.assertContains(self.response, 'href="{0}"'.format(homepage_url))

    def test_board_topics_view_contains_navigation_links(self):
        response = self.client.get(self.board_topics_url)
        # 测试话题列表页包含指向主页和创建新话题的链接
        self.assertContains(response, 'href="{0}"'.format(self.homepage_url))
        self.assertContains(response, 'href="{0}"'.format(self.new_topic_url))