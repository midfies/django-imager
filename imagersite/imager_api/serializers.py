from rest_framework import serializers
from django.contrib.auth.models import User
from imager_images.models import Photo, Album


# class SnippetSerializer(serializers.HyperlinkedModelSerializer):
#     owner = serializers.ReadOnlyField(source='owner.username')
#     highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

#     class Meta:
#         model = Snippet
#         fields = ('url', 'id', 'highlight', 'owner',
#                   'title', 'code', 'linenos', 'language', 'style')


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

#     class Meta:
#         model = User
#         fields = ('url', 'id', 'username', 'snippets')

class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(many=False, view_name='user_photo_list', read_only=True)
    # albums = serializers.HyperlinkedRelatedField(many=True, view_name='album_photo_list', read_only=True)
    photo = serializers.HyperlinkedRelatedField(many=False, view_name='just_photo', read_only=True)

    class Meta:
        model = Photo
        fields = ('title',
                  'description',
                  'date_uploaded',
                  'date_published',
                  'date_modified',
                  'published',
                  'photo',
                  'owner',
                  'albums',
                  'tags')
