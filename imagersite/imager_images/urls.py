"""Routes for albums and photos."""
from django.conf.urls import url
from imager_images.models import Photo
from imager_images.views import (
    AlbumView,
    PhotoView,
    AlbumGalleryView,
    PhotoGalleryView,
    LibraryView,
    AddAlbumView,
    AddPhotoView,
    EditAlbumView,
    EditPhotoView,
)
from django.views.generic import DetailView

urlpatterns = [
    url(r'^library/$', LibraryView.as_view(), name='library'),
    url(r'albums/(?P<albumid>\d+)/$', AlbumView.as_view(), name='album'),
    url(r'albums/$', AlbumGalleryView.as_view(), name='album_gallery'),
    url(r'photos/$', PhotoGalleryView.as_view(), name='photo_gallery'),
    url(r'photos/(?P<pk>\d+)/$', PhotoView.as_view(), name='photo'),
    url(r'albums/add/$', AddAlbumView.as_view(), name='add_album'),
    url(r'photos/add/$', AddPhotoView.as_view(), name='add_photo'),
    url(r'albums/(?P<pk>\d+)/edit/$', EditAlbumView.as_view(), name='edit_album'),
    url(r'photos/(?P<pk>\d+)/edit/$', EditPhotoView.as_view(), name='edit_photo'),
]
