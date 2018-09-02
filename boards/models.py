from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    name        = models.CharField('名称', max_length=30, unique=True)
    description = models.CharField('描述信息', max_length=100)

    def __str__(self):
        return self.name


class Topic(models.Model):
    subject      = models.CharField('主题',max_length=255)
    last_updated = models.DateTimeField('最近更新时间',auto_now_add=True)
    board        = models.ForeignKey(Board, related_name='topics', verbose_name='所属板块')
    starter      = models.ForeignKey(User, related_name='topics', verbose_name='创建用户')


class Post(models.Model):
    message    = models.TextField(max_length=4000)
    topic      = models.ForeignKey(Topic, related_name='posts', verbose_name='主题')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('最近更新时间', null=True)
    created_by = models.ForeignKey(User, related_name='posts', verbose_name='创建用户')
    updated_by = models.ForeignKey(User, null=True, related_name='+')