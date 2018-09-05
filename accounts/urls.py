from django.conf.urls import include, url
from accounts.views import UserUpdateView

urlpatterns = [
    url(r'^account/$', UserUpdateView.as_view(), name='my_account'),
]
