from django.conf.urls import include, url
from .views import (home, board_topics, new_topic, topic_posts, reply_topic, 
                    PostUpdateView, NewPostView, PostListView, TopicListView)

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^boards/(?P<pk>\d+)/$', TopicListView.as_view(), name='topics'),
    url(r'^boards/(?P<pk>\d+)/new/$', new_topic, name='new_topic'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', PostListView.as_view(), name='topic_posts'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', reply_topic, name='reply_topic'),

    url(r'^new_post/$', NewPostView.as_view(), name='new_post'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$',
        PostUpdateView.as_view(), name='edit_post'),
]
