from django.conf.urls import url
from imager_images import views

urlpatterns = [
    url(r'^library/$', views.library_view, name='library'),
    url(r'albums/(?P<albumid>\d+)/$', views.album_view, name='album'),
    url(r'albums/$', views.album_gallery_view, name='album_gallery'),
    url(r'photos/$', views.photo_gallery_view, name='photo_gallery'),
    url(r'photos/(?P<photoid>\d+)/$', views.photo_view, name='photo'),
]
