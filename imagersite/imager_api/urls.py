"""URL patterns."""

from django.conf.urls import url
from imager_api.views import PhotoViewSet, AlbumViewSet


urlpatterns = [
    url(r'^photos/$', PhotoViewSet.as_view({'get': 'list'}), name='photo_list'),
    url(r'^albums/$', AlbumViewSet.as_view({'get': 'list'}), name='album_list'),
]
