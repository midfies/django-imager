from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
from imager_images.models import Photo, Album
from imager_profile.tests import UserFactory
import factory
from faker import Faker
from bs4 import BeautifulSoup


class UserFactory(factory.django.DjangoModelFactory):
        """User factory for testing."""

        class Meta:
            """Model meta."""

            model = User

        username = factory.Sequence(lambda n: "User{}".format(n))
        email = factory.LazyAttribute(
            lambda x: "{}@imager.com".format(x.username.replace(" ", ""))
        )


class PhotoFactory(factory.django.DjangoModelFactory):
        """User factory for testing."""

        class Meta:
            """Model meta."""

            model = Photo

        owner = billy
        title = factory.Sequence(lambda n: "photo{}".format(n))


class AlbumFactory(factory.django.DjangoModelFactory):
        """User factory for testing."""

        class Meta:
            """Model meta."""

            model = Album

        title = factory.Sequence(lambda n: "album{}".format(n))


class PhotoAlbumBackendTests(TestCase):
    """The Profile Model test runner for db stuff."""

    def setUp(self):
        """The appropriate setup for the appropriate test."""
        self.photos = [PhotoFactory.create() for i in range(20)]

    def test_can_add_photos_to_album(self):
        """Photos can be associated with albums."""
        photo = self.photos[0]
        album = AlbumFactory()
        album.owner = photo.owner
        album.photos.add(photo)
        album.save()
        self.assertTrue(album.photos.first() is photo)
