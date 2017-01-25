"""Routes for albums and photos."""
from django.conf.urls import url
from imager_images.models import Photo
from imager_images.views import AlbumView, AlbumGalleryView, PhotoGalleryView, LibraryView
from django.views.generic import DetailView

urlpatterns = [
    url(r'^library/$', LibraryView.as_view(), name='library'),
    url(r'albums/(?P<albumid>\d+)/$', AlbumView.as_view(), name='album'),
    url(r'albums/$', AlbumGalleryView.as_view(), name='album_gallery'),
    url(r'photos/$', PhotoGalleryView.as_view(), name='photo_gallery'),
    url(r'photos/(?P<pk>\d+)/$', DetailView.as_view(
        template_name="imager_images/photo.html",
        model=Photo
    ), name='photo'),
]
