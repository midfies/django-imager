"""Tests for the imager app."""
from django.test import TestCase
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
import factory

# Create your tests here.


class ProfileTestCase(TestCase):
    """The Profile Model test runner."""

    class UserFactory(factory.django.DjangoModelFactory):
        """User factory for testing."""

        class Meta:
            """Model meta."""

            model = User

        username = factory.Sequence(lambda n: "User{}".format(n))
        email = factory.LazyAttribute(
            lambda x: "{}@imager.com".format(x.username.replace(" ", ""))
        )

    def setUp(self):
        """The appropriate setup for the appropriate test."""
        self.users = [self.UserFactory.create() for i in range(20)]

    def test_profile_is_made_when_user_is_saved(self):
        """."""
        self.assertTrue(ImagerProfile.objects.count() == 20)

    def test_profile_is_associated_with_actual_users(self):
        """."""
        profile = ImagerProfile.objects.first()
        self.assertTrue(hasattr(profile, "user"))
        self.assertIsInstance(profile.user, User)

    def test_user_has_profile_attached(self):
        """."""
        user = self.users[0]
        self.assertTrue(hasattr(user, "profile"))
        self.assertIsInstance(user.profile, ImagerProfile)

    def test_active_model_manager_returns_query_set_of_profiles(self):
        """Test that active model manager returns profil query set."""
        query = ImagerProfile.active.all()
        self.assertIsInstance(query[0], ImagerProfile)

    def test_updating_profile_works(self):
        """Test that updating profile updates the db."""
        user = self.users[0]
        user.profile.bio = "This is the new bio."
        query = User.objects.first()
        import pdb; pdb.set_trace()
        self.assertTrue(query.profile.bio == "This is the new bio.")
