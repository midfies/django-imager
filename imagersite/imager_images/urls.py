from django.conf.urls import url
from imager_images import views

urlpatterns = [
    url(r'^library/$', views.library_view, name='library'),
    url(r'albums/(?P<albumid>\d+)/$', views.album_view, name='album'),
    url(r'photos/$', views.album_view, name='photos'),
    url(r'photos/(?P<photoid>\d+)/$', views.album_view, name='photo'),
]
