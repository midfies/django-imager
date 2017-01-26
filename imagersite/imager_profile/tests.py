"""Tests for the imager app."""
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
from imager_profile.views import EditProfileView
import factory
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


# class ProfileBackendTests(TestCase):
#     """The Profile Model test runner for db stuff."""

#     def setUp(self):
#         """The appropriate setup for the appropriate test."""
#         self.users = [UserFactory.create() for i in range(20)]

#     def test_profile_is_made_when_user_is_saved(self):
#         """."""
#         self.assertTrue(ImagerProfile.objects.count() == 20)

#     def test_profile_is_associated_with_actual_users(self):
#         """."""
#         profile = ImagerProfile.objects.first()
#         self.assertTrue(hasattr(profile, "user"))
#         self.assertIsInstance(profile.user, User)

#     def test_user_has_profile_attached(self):
#         """."""
#         user = self.users[0]
#         self.assertTrue(hasattr(user, "profile"))
#         self.assertIsInstance(user.profile, ImagerProfile)

#     def test_active_model_manager_returns_query_set_of_profiles(self):
#         """Test that active model manager returns profil query set."""
#         query = ImagerProfile.active.all()
#         self.assertIsInstance(query[0], ImagerProfile)

#     def test_active_model_manager(self):
#         """With one user set inactive, there should be one less active profile."""
#         user = self.users[0]
#         user.is_active = False
#         user.save()
#         self.assertEqual(ImagerProfile.active.count(),
#                          ImagerProfile.objects.count() - 1)

#     def test_can_update_profile_through_user(self):
#         """Test updating profile through user updates the corresponding profile."""
#         user = User.objects.first()
#         user.profile.bio = 'WOOHOO'
#         user.profile.save()
#         profile = ImagerProfile.objects.get(user=user)
#         self.assertEqual(user.profile.bio, profile.bio)

#     def test_link_between_user_and_profile(self):
#         """Test updating profile updates the corresponding user's profile."""
#         user = User.objects.first()
#         profile = ImagerProfile.objects.get(user=user)
#         profile.bio = 'WOOHOO'
#         profile.save()
#         self.assertEqual(user.profile.bio, profile.bio)


class ProfileFrontendTests(TestCase):
    """Test profile views and routes and stuff."""

    def setUp(self):
        """Set up test tool instances."""
        self.client = Client()
        self.request = RequestFactory()

    def add_billy(self):
        """Make Billy and return his profile."""
        user = UserFactory.create()
        user.username = 'BillyTheGoat'
        user.set_password('billyspassword')
        user.save()
        return user.profile

    def register_billy(self, follow=False):
        response = self.client.post('/accounts/register/', {
            'username': 'BillyThePig',
            'email': 'oink@oink.com',
            'password1': 'billyspasswordoink',
            'password2': 'billyspasswordoink'
        }, follow=follow)
        return response

#     def test_profile_view_status_ok(self):
#         """Test profile view for billy is a thing."""
#         self.add_billy()
#         req = self.request.get('/wat')
#         response = profile_view(req, 'BillyTheGoat')
#         self.assertEqual(response.status_code, 200)

#     def test_profile_route_status_ok(self):
#         """Not sure why this response needs to be followed, but it does."""
#         self.add_billy()
#         response = self.client.get('/profile/BillyTheGoat', follow=True)
#         self.assertEqual(response.status_code, 200)

#     def test_profile_view_context(self):
#         """Assert that photos is passed in context, and that billy has no photos."""
#         self.add_billy()
#         response = self.client.get('/profile/BillyTheGoat', follow=True)
#         self.assertEqual(response.context['photos'].count(), 0)

#     def test_profile_users_right_templates(self):
#         self.add_billy()
#         response = self.client.get('/profile/BillyTheGoat', follow=True)
#         self.assertTemplateUsed(response, 'imager_profile/profile.html')
#         self.assertTemplateUsed(response, 'base.html')

#     def test_login_route_form(self):
#         """Login should have the right inputs and stuff."""
#         response = self.client.get('/login/')
#         soup = BeautifulSoup(response.rendered_content, 'html.parser')
#         inputs = soup.find_all('input')
#         self.assertEqual(len(inputs), 3)

#     def test_login_route_post(self):
#         """Test billy login redirects."""
#         self.add_billy()
#         response = self.client.post('/login/', {
#             'username': 'BillyTheGoat',
#             'password': 'billyspassword'
#         })
#         self.assertEqual(response.status_code, 302)

#     def test_login_post_redirects_to_homepage(self):
#         """Should redirect to homepage."""
#         self.add_billy()
#         response = self.client.post('/login/', {
#             'username': 'BillyTheGoat',
#             'password': 'billyspassword'
#         }, follow=True)
#         self.assertEqual(response.redirect_chain[0][0], '/')

#     def test_register_form(self):
#         """Register page should have 5 inputs."""
#         response = self.client.get('/accounts/register/')
#         soup = BeautifulSoup(response.rendered_content, 'html.parser')
#         inputs = soup.find_all('input')
#         self.assertEqual(len(inputs), 5)

#     def test_can_register_new_user_status_code(self):
#         """Should get 302 to register complete after successful registration."""
#         response = self.register_billy()
#         self.assertEqual(response.status_code, 302)

#     def test_can_register_new_user_redirect_to_complete(self):
#         """Should redirect to registration complete after registration."""
#         response = self.register_billy(follow=True)
#         self.assertEqual(response.redirect_chain[0][0], '/accounts/register/complete/')
#         self.assertTemplateUsed(response, 'registration/registration_complete.html')

#     def test_registered_user_in_db(self):
#         """Should be able to query new user."""
#         self.assertEqual(ImagerProfile.objects.count(), 0)
#         self.register_billy(follow=True)
#         self.assertEqual(ImagerProfile.objects.count(), 1)

#     def test_registered_user_inactive(self):
#         """New user should start out inactive."""
#         self.register_billy(follow=True)
#         billy = ImagerProfile.objects.first()
#         self.assertFalse(billy.is_active)

    def test_edit_prfile(self):
        billy = self.add_billy()
        self.register_billy()
        self.client.force_login(billy.user)
        request = self.request.get('/')
        request.user = billy.user
        response = EditProfileView.as_view()(request)
        import pdb; pdb.set_trace()
