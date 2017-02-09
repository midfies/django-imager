
"""Serializing and deserializing the photo instances into json."""

from rest_framework import serializers
from imager_images.models import Photo, Album


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Photos."""

    owner = serializers.ReadOnlyField(source='owner.user.username')

    class Meta:
        """Meta for Photo serializer."""

        model = Photo
        fields = ('owner', 'title', 'description', 'date_uploaded',
                  'date_modified', 'date_published', 'published', 'photo')


class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Albums."""

    owner = serializers.ReadOnlyField(source='owner.user.username')
    photos = PhotoSerializer(many=True)
    cover_photo = PhotoSerializer()

    class Meta:
        """Meta for Album serializer."""

        model = Album
        fields = ('owner', 'title', 'description', 'date_uploaded',
                  'date_modified', 'date_published', 'published', 'photos', 'cover_photo')
