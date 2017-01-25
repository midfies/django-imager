"""URLS for profile routes."""
from django.conf.urls import url
from imager_profile.views import ProfileView, ProfileUserView

urlpatterns = [
    url(r'(?P<slug>\w+)/$', ProfileView.as_view(), name='profile'),
    url(r'^$', ProfileUserView.as_view(), name='profile_user'),
]
