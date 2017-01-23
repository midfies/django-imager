from django.conf.urls import url
from imager_images import views

urlpatterns = [
    url(r'^$', views.library_view, name='library'),
    url(r'(?P<albumid>\d+)/$', views.album_view, name='album'),
]
