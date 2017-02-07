from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from imager_api import views

urlpatterns = [
    url(r'profile/(?P<pk>\d+)/photos/$', views.UserPhotoList.as_view(), name='user_photo_list'),
    url(r'^photo/(?P<pk>\d+)/$', views.Photo.as_view(), name='just_photo'),
]

urlpatterns = format_suffix_patterns(urlpatterns)