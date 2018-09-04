from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator


class Board(models.Model):
    name        = models.CharField('名称', max_length=30, unique=True)
    description = models.CharField('描述信息', max_length=100)

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()


class Topic(models.Model):
    subject      = models.CharField('主题',max_length=255)
    last_updated = models.DateTimeField('最近更新时间',auto_now_add=True)
    board        = models.ForeignKey(Board, related_name='topics', verbose_name='所属板块')
    starter      = models.ForeignKey(User, related_name='topics', verbose_name='创建用户')
    views        = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject



class Post(models.Model):
    message    = models.TextField()
    topic      = models.ForeignKey(Topic, related_name='posts', verbose_name='主题')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('最近更新时间', null=True)
    created_by = models.ForeignKey(User, related_name='posts', verbose_name='创建用户')
    updated_by = models.ForeignKey(User, null=True, related_name='+')

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)