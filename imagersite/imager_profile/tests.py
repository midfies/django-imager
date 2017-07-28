"""Tests for the imager app."""
import factory
from bs4 import BeautifulSoup
from django.test import TestCase, Client, RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile

from django.contrib.auth.models import User
from imager_images.models import Album, Photo
from imager_profile.models import ImagerProfile

from imager_profile.views import EditProfileView
from imager_profile.forms import EditProfileForm


class UserFactory(factory.django.DjangoModelFactory):
    """User with profile factory."""

    class Meta:
        """Model meta."""

        model = User

    username = factory.Sequence(lambda n: "User{}".format(n))
    # profile = ImagerProfile()
    email = factory.LazyAttribute(
        lambda x: "{}@imager.com".format(x.username.replace(" ", ""))
    )


class PhotoFactory(factory.django.DjangoModelFactory):
        """Photo factory for testing."""

        class Meta:
            """Model meta."""

            model = Photo

        title = factory.Sequence(lambda n: "photo{}".format(n))
        photo = SimpleUploadedFile('test.jpg', open('imager_images/static/generic.jpg', 'rb').read())


class AlbumFactory(factory.django.DjangoModelFactory):
        """Album factory for testing."""

        class Meta:
            """Model meta."""

            model = Album

        title = factory.Sequence(lambda n: "album{}".format(n))


class ProfileModelTests(TestCase):
    """Unit test ImagerProfile model."""

    def setUp(self):
        """Add some photos."""
        self.photos = [PhotoFactory.create() for i in range(10)]
        self.albums = [AlbumFactory.create() for i in range(2)]
        for i, photo in enumerate(self.photos):
            self.albums[i // 5].photos.add(photo)

    def add_profile(self, **kwargs):
        """Add profile to db."""
        user = UserFactory.create()
        profile = user.profile
        for kwarg in kwargs:
            if kwarg == 'username':
                user.username = kwargs[kwarg]
            else:
                setattr(profile, kwarg, kwargs[kwarg])
        user.save()
        profile.save()

    def test_can_add_profile(self):
        """Assure a profile can be added and retrieved."""
        count_before = ImagerProfile.objects.count()
        self.add_profile()
        self.assertEqual(ImagerProfile.objects.count() - count_before, 1)

    def test_last_profile_is_last_added(self):
        """Test last profile added is same when retrieved by title or by last."""
        self.add_profile(username='billyboythorn')
        self.assertEqual(
            ImagerProfile.objects.get(user__username='billyboythorn'),
            ImagerProfile.objects.last()
        )

    def test_can_add_profile_with_fields(self):
        """Assure profiles can be added and retrieved with fields attached."""
        fields = {
            'camera_type': 'Nikon',
            'address': '245 Qwerty Dr, Seattle WA 98189',
            'bio': 'long story short',
            'website': 'www.com',
            'hireable': False,
            'travel_radius': 2,
            # 'phone': '19496001323',
            'type_of_photography': 'top notch',
        }
        self.add_profile(**fields)
        profile = ImagerProfile.objects.last()
        for field in fields:
            self.assertEqual(getattr(profile, field), fields[field])

    def test_profiles_default_fields(self):
        """Test profile models default fields are valid."""
        self.add_profile()
        profile = ImagerProfile.objects.last()
        self.assertEqual(profile.hireable, True)

    def test_user_attached_to_profile(self):
        """Assert that profile attached to user."""
        self.add_profile()
        self.assertEqual(
            ImagerProfile.objects.last(),
            User.objects.last().profile
        )
        self.assertEqual(
            ImagerProfile.objects.last().user,
            User.objects.last()
        )

    def test_can_add_photos_to_profile(self):
        """Assert photos can be associated with profiles."""
        self.add_profile()
        photos = Photo.objects.all()
        self.assertGreater(photos.count(), 0)
        profile = ImagerProfile.objects.last()
        for photo in photos:
            profile.photos.add(photo)
        profile.save()
        self.assertListEqual(
            list(profile.photos.all()),
            list(photos)
        )
        for photo in Photo.objects.all():
            self.assertEqual(photo.owner, profile)

    def test_can_add_albums_to_profile(self):
        """Assert albums can be associated with profile."""
        self.add_profile()
        albums = Album.objects.all()
        self.assertGreater(albums.count(), 0)
        profile = ImagerProfile.objects.last()
        for album in albums:
            profile.albums.add(album)
        profile.save()
        self.assertListEqual(
            list(profile.albums.all()),
            list(albums)
        )
        for album in Album.objects.all():
            self.assertEqual(album.owner, profile)


# class ProfileBackendTests(TestCase):
#     """The Profile Model test runner for db stuff."""

#     def setUp(self):
#         """The appropriate setup for the appropriate test."""
#         self.users = [UserFactory.create() for i in range(20)]

#     def test_profile_str_method_produces_username(self):
#         """Test that the string method for the profile prints the user."""
#         the_user = User.objects.first()
#         # import pdb; pdb.set_trace()
#         self.assertTrue(str(the_user.profile) == the_user.username)

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


# class ProfileFrontendTests(TestCase):
#     """Test profile views and routes and stuff."""

#     def setUp(self):
#         """Set up test tool instances."""
#         self.client = Client()
#         self.request = RequestFactory()

#     def add_billy(self):
#         """Make Billy and return his profile."""
#         user = UserFactory.create()
#         user.username = 'BillyTheGoat'
#         user.set_password('billyspassword')
#         user.save()
#         return user.profile

#     def register_billy(self, follow=False):
#         response = self.client.post('/accounts/register/', {
#             'username': 'BillyThePig',
#             'email': 'oink@oink.com',
#             'password1': 'billyspasswordoink',
#             'password2': 'billyspasswordoink'
#         }, follow=follow)
#         return response

#     def test_home_route_is_status_ok(self):
#         """Funcional test."""
#         response = self.client.get("/")
#         self.assertTrue(response.status_code == 200)

#     def test_home_view_returns_status_ok(self):
#         """Test that the home view returns a status 200 code."""
#         from imagersite.views import HomeView
#         request = self.request.get('/')
#         view = HomeView.as_view()
#         response = view(request)
#         self.assertEqual(response.status_code, 200)

#     def test_home_route_uses_correct_template(self):
#         """Test that the home view renders the home.html template."""
#         response = self.client.get("/")
#         self.assertTemplateUsed(response, "base.html")
#         self.assertTemplateUsed(response, "imagersite/home.html")

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

#     def test_profile_route_without_username_leads_to_logged_in_profile(self):
#         """Test not specifying a username of profile route goes to logged in user's profile."""
#         self.add_billy()
#         self.client.login(username='BillyTheGoat', password='billyspassword')
#         response = self.client.get('/profile/', follow=True)
#         self.assertContains(response, '<title>BillyTheGoat\'s Profile</title>')

#     def test_profile_route_status_ok(self):
#         """Not sure why this response needs to be followed, but it does."""
#         self.add_billy()
#         response = self.client.get('/profile/BillyTheGoat', follow=True)
#         self.assertEqual(response.status_code, 200)

#     def test_profile_users_right_templates(self):
#         """Test that the user profile uses the correct templates."""
#         self.add_billy()
#         response = self.client.get('/profile/BillyTheGoat', follow=True)
#         self.assertTemplateUsed(response, 'imager_profile/profile.html')
#         self.assertTemplateUsed(response, 'base.html')

#     def test_edit_profile_renders(self):
#         """Test that the edit profile renders."""
#         self.add_billy()
#         self.client.login(username='BillyTheGoat', password='billyspassword')
#         response = self.client.get('/profile/edit', follow=True)
#         self.assertContains(response, '<h2>Edit your profile.</h2>')
#         self.assertEqual(response.status_code, 200)

#     def test_edit_profile_form_valid(self):
#         profile = self.add_billy()
#         form = EditProfileForm(instance=profile, data={
#             'camera_type': 'CANNON',
#             'address': '166 There St',
#             'bio': 'This is a bio',
#             'website': 'website@website.com',
#             'hireable': 'True',
#             'travel_radius': 1.0,
#             'type_of_photography': 'NATURE',
#             'First Name': 'Billy',
#             'Last Name': 'The Goat',
#             'Email': 'this@that.com'
#         })
#         self.assertTrue(form.is_valid())

#     def test_edit_profile_form_invalid(self):
#         profile = self.add_billy()
#         form = EditProfileForm(instance=profile, data={
#             'camera_type': 'Baluga',
#             'address': '166 There St',
#             'bio': 'This is a bio',
#             'website': 'website@website.com',
#             'hireable': 'True',
#             'travel_radius': 1.0,
#             'type_of_photography': 'NATURE',
#             'First Name': 'Billy',
#             'Last Name': 'The Goat',
#             'Email': 'this@that.com'
#         })
#         self.assertFalse(form.is_valid())

#     def test_edit_profile_changes_profile(self):
#         """Test that edit profile changes profile."""
#         test_user = self.add_billy()
#         self.client.force_login(test_user.user)
#         self.client.post("/profile/edit/", {
#             'camera_type': 'CANNON',
#             'address': '166 There St',
#             'bio': 'This is a bio',
#             'website': 'website@website.com',
#             'hireable': 'True',
#             'travel_radius': 1.0,
#             'type_of_photography': 'NATURE',
#             'First Name': 'Billy',
#             'Last Name': 'The Goat',
#             'Email': 'this@that.com'
#         })
#         user = User.objects.first()
#         self.assertTrue(user.profile.camera_type == 'CANNON')
