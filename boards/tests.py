import django
from django.urls import resolve
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from .views import home, board_topics, new_topic
from .models import Board, Topic, Post
from .forms import NewTopicForm

# TODO: Configure your database in settings.py and sync before running tests.

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
        self.assertEquals(view.func, board_topics) # 测试话题列表页调用正确的视图函数

    def test_board_topics_view_contains_link_back_to_homepage(self):
        # 测试版块页包含指向首页的链接
        homepage_url = reverse('boards:home')
        self.assertContains(self.response, 'href="{0}"'.format(homepage_url))

    def test_board_topics_view_contains_navigation_links(self):
        response = self.client.get(self.board_topics_url)
        # 测试话题列表页包含指向主页和创建新话题的链接
        self.assertContains(response, 'href="{0}"'.format(self.homepage_url))
        self.assertContains(response, 'href="{0}"'.format(self.new_topic_url))



class NewTopicTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        django.setup()

    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')
        User.objects.create_user(username='john', email='john@doe.com', password='123')
        self.board_topics_url = reverse('boards:topics', kwargs={'pk': 1})
        self.new_topic_url = reverse('boards:new_topic', kwargs={'pk': 1})
        self.homepage_url = reverse('boards:home')

    def test_new_topic_view_success_status_code(self):
        response = self.client.get(self.new_topic_url)
        self.assertEquals(response.status_code, 200) # 测试new_topic页正确返回

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('boards:new_topic', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404) # 测试给不存在的主题添加topic时返回404

    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve(self.new_topic_url)
        self.assertEquals(view.func, new_topic) # 测试新增话题页调用正确的视图函数

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        # 测试新增话题页包含指向话题列表的链接
        response = self.client.get(self.new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(self.board_topics_url))

    def test_csrf(self):
        url = reverse('boards:new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken') # 确保页面中包含csrf_token

    def test_new_topic_valid_post_data(self):
        url = reverse('boards:new_topic', kwargs={'pk': 1})
        data = {
            'subject': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        # 确保在提交数据后，Topic和Post实例被创建
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('boards:new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        
        self.assertEquals(response.status_code, 200)

    def test_new_topic_invalid_post_data_empty_fields(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('boards:new_topic', kwargs={'pk': 1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        form = response.context.get('form') # 抓取上下文的表单实例
        self.assertTrue(form.errors)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

        
    def test_contains_form(self):
        response = self.client.get(self.new_topic_url)
        form = response.context.get('form') # 抓取上下文的表单实例
        self.assertIsInstance(form, NewTopicForm)