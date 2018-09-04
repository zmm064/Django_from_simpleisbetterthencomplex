from django.conf.urls import include, url
from .views import home, board_topics, new_topic, topic_posts, reply_topic

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^boards/(?P<pk>\d+)/$', board_topics, name='topics'),
    url(r'^boards/(?P<pk>\d+)/new/$', new_topic, name='new_topic'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', topic_posts, name='topic_posts'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', reply_topic, name='reply_topic'),
]
