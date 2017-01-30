"""URLS for profile routes."""
from django.conf.urls import url
from imager_profile.views import ProfileView, ProfileUserView, EditProfileView

urlpatterns = [
    url(r'edit/$', EditProfileView.as_view(), name='edit_profile'),
    url(r'(?P<slug>\w+)/$', ProfileView.as_view(), name='profile'),
    url(r'^$', ProfileUserView.as_view(), name='profile_user'),
]
