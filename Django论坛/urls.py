"""
Definition of urls for Django论坛.
"""

from django.conf.urls import include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('boards.urls', namespace='boards')),
]
