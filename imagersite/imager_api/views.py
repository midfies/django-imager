"""View API endpoint."""

from rest_framework import viewsets
from imager_images.models import Photo, Album
from imager_api.serializers import PhotoSerializer, AlbumSerializer
from django.urls import reverse_lazy
from rest_framework.permissions import IsAuthenticated


class PhotoViewSet(viewsets.ModelViewSet):
    """API endpoint for photo views."""
    permission_classes = (IsAuthenticated,)
    serializer_class = PhotoSerializer
    login_url = reverse_lazy("login")

    def get_queryset(self):
        """Get queryset for photos of owner."""
        return Photo.objects.filter(owner=self.request.user.profile)


class AlbumViewSet(viewsets.ModelViewSet):
    """API endpoint for album views."""
    permission_classes = (IsAuthenticated,)
    serializer_class = AlbumSerializer
    login_url = reverse_lazy("login")

    def get_queryset(self):
        """Get queryset for albums of owner."""
        return Album.objects.filter(owner=self.request.user.profile)