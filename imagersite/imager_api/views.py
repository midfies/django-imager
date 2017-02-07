from imager_images.models import Photo
from imager_profile.models import ImagerProfile
from imager_api.serializers import PhotoSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import renderers


class UserPhotoList(generics.ListCreateAPIView):
    serializer_class = PhotoSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        profile = ImagerProfile.active.get(pk=self.kwargs.get('pk'))
        if profile.user == self.request.user:
            return profile.photos.all()
        else:
            return profile.photos.filter(published='PUBLIC')


class Photo(generics.GenericAPIView):
    queryset = Photo.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        photo = self.get_object()
        return Response(photo)