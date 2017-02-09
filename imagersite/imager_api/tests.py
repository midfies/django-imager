from django.test import TestCase, Client, RequestFactory
from django.urls import reverse_lazy
from django.core.files.uploadedfile import SimpleUploadedFile
from imager_images.models import Photo, Album
from imager_profile.tests import UserFactory
from imager_api.views import PhotoViewSet, AlbumViewSet
import factory


class PhotoFactory(factory.django.DjangoModelFactory):
        """User factory for testing."""

        class Meta:
            """Model meta."""

            model = Photo

        title = factory.Sequence(lambda n: "photo{}".format(n))
        photo = SimpleUploadedFile('test.jpg', open('imager_images/static/generic.jpg', 'rb').read())


class AlbumFactory(factory.django.DjangoModelFactory):
        """User factory for testing."""

        class Meta:
            """Model meta."""

            model = Album

        title = factory.Sequence(lambda n: "album{}".format(n))


class ImagerAPITests(TestCase):
    """The Profile Model test runner for db stuff."""

    def setUp(self):
        """The appropriate setup for the appropriate test."""
        self.client = Client()
        self.request = RequestFactory()
        self.users = [UserFactory.create() for i in range(20)]
        self.photos = [PhotoFactory.create() for i in range(20)]
        self.albums = [AlbumFactory.create() for i in range(20)]

    def add_test_user(self):
        """Make test user and return his profile."""
        user = UserFactory.create()
        user.username = 'BillyTheGoat'
        user.set_password('billyspassword')
        photo = PhotoFactory.create()
        photo.owner = user.profile
        user.save()
        photo.save()
        return user

    def test_api_photo_route_is_status_ok(self):
        """Test that the api photo route produces a status ok."""
        test_user = self.add_test_user()
        self.client.force_login(test_user)
        request = self.request.get(reverse_lazy("photo_list"))
        request.user = test_user
        view = PhotoViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertTrue(response.status_code == 200)

    def test_api_album_route_is_status_ok(self):
        """Test that the api album route produces a status ok."""
        test_user = self.add_test_user()
        self.client.force_login(test_user)
        request = self.request.get(reverse_lazy("album_list"))
        request.user = test_user
        view = AlbumViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertTrue(response.status_code == 200)

    def test_user_can_view_photos_in_api(self):
        """Test the user can access the api endpoint of their photos."""
        test_user = self.add_test_user()
        photo = self.photos[0]
        photo.owner = test_user.profile
        photo.title = 'easter egg'
        photo.save()
        self.client.force_login(test_user)
        request = self.request.get(reverse_lazy("photo_list"))
        request.user = test_user
        view = PhotoViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertTrue(b'easter egg' in response.rendered_content)

    def test_user_can_view_albums_in_api(self):
        """Test the user can access the api endpoint of their albums."""
        test_user = self.add_test_user()
        album = self.albums[0]
        album.owner = test_user.profile
        album.title = 'easter egg'
        album.save()
        self.client.force_login(test_user)
        request = self.request.get(reverse_lazy("album_list"))
        request.user = test_user
        view = AlbumViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertTrue(b'easter egg' in response.rendered_content)

    def test_non_user_cannot_view_photos_in_api(self):
        """Test non user cannnot access the api endpoint of photos."""
        request = self.request.get(reverse_lazy("photo_list"))
        view = PhotoViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertTrue(b"Authentication credentials were not provided." in response.rendered_content)

    def test_non_user_cannot_view_album_in_api(self):
        """Test non user cannnot access the api endpoint of albums."""
        request = self.request.get(reverse_lazy("album_list"))
        view = AlbumViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertTrue(b"Authentication credentials were not provided." in response.rendered_content)

