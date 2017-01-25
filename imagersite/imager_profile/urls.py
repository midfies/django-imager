"""URLS for profile routes."""
from django.conf.urls import url
from imager_profile.views import ProfileView

urlpatterns = [
    url(r'(?P<username>\w+)/$', ProfileView.as_view(), name='profile'),
    url(r'^$', ProfileView.as_view(), {'username': 'USER'}, name='profile'),
]
