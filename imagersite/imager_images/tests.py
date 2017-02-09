from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.core.files.uploadedfile import SimpleUploadedFile
from imager_profile.models import ImagerProfile
from imager_images.models import Photo, Album
from imager_profile.tests import UserFactory
import factory
from bs4 import BeautifulSoup as Soup


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


class PhotoAlbumTests(TestCase):
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

    def add_photo_to_user(self, tags='', follow=False, published='PUBLIC'):
        """Upload a photo for a user."""
        response = self.client.post("/images/photos/add/", {
            'title': 'A Test Photo',
            'description': 'Test Description for photo',
            'published': published,
            'photo': SimpleUploadedFile('test.jpg', open('imager_images/static/generic.jpg', 'rb').read()),
            'tags': tags
        }, follow=follow)
        return response

    def test_can_add_photos_to_album(self):
        """Photo can be associated with albums."""
        photo = self.photos[0]
        album = AlbumFactory()
        album.owner = photo.owner
        album.photos.add(photo)
        album.save()
        self.assertTrue(album.photos.first() == photo)

    def test_library_route_is_status_ok(self):
        """Test that library view status code is 200."""
        from imager_images.views import LibraryView
        test_user = self.add_test_user()
        self.client.force_login(test_user)
        request = self.request.get(reverse_lazy("library"))
        request.user = test_user
        view = LibraryView.as_view()
        response = view(request)
        self.assertTrue(response.status_code == 200)

    def test_library_view_uses_correct_template(self):
        """Test that library view uses the correct template."""
        test_user = self.add_test_user()
        self.client.force_login(test_user)
        request = self.client.get("/images/library/")
        request.user = test_user
        self.assertTemplateUsed(request, 'imager_images/library.html')

    def test_album_gallery_route_is_status_ok(self):
        """Test that album gallery view status code is 200."""
        from imager_images.views import AlbumGalleryView
        request = self.request.get(reverse_lazy("album_gallery"))
        view = AlbumGalleryView.as_view()
        response = view(request)
        self.assertTrue(response.status_code == 200)

    def test_album_gallery_uses_correct_template(self):
        """Test that album gallery view uses the correct template."""
        request = self.client.get("/images/albums/")
        self.assertTemplateUsed(request, 'imager_images/album_gallery.html')

    def test_photo_gallery_route_is_status_ok(self):
        """Test that photo gallery view status code is 200t."""
        from imager_images.views import PhotoGalleryView
        request = self.request.get(reverse_lazy("photo_gallery"))
        view = PhotoGalleryView.as_view()
        response = view(request)
        self.assertTrue(response.status_code == 200)

    def test_photo_gallery_uses_correct_template(self):
        """Test that photo gallery view uses the correct template."""
        request = self.client.get("/images/photos/")
        self.assertTemplateUsed(request, 'imager_images/photo_gallery.html')

    def test_add_photo_route_is_status_ok(self):
        """Test that add photo view status code is 200."""
        from imager_images.views import AddPhotoView
        test_user = self.add_test_user()
        self.client.force_login(test_user)
        request = self.request.get(reverse_lazy("add_photo"))
        request.user = test_user
        view = AddPhotoView.as_view()
        response = view(request)
        self.assertTrue(response.status_code == 200)

    def test_add_photo_view_uses_correct_template(self):
        """Test that add photo view uses the correct template."""
        test_user = self.add_test_user()
        self.client.force_login(test_user)
        request = self.client.get("/images/photos/add/")
        request.user = test_user
        self.assertTemplateUsed(request, 'imager_images/add_photo.html')

    def test_add_photo_submission_changes_owner(self):
        """Test that submitting a new photo changes the owner."""
        test_user = self.add_test_user()
        self.client.force_login(test_user)
        self.add_photo_to_user()
        photo = Photo.public.first()
        self.assertTrue(photo.owner == test_user.profile)

    def test_add_album_submission_changes_owner(self):
        """Test that submitting a new album changes the owner."""
        test_user = self.add_test_user()
        self.client.force_login(test_user)
        photo = Photo()
        photo.owner = test_user.profile
        photo.save()

        self.client.post("/images/albums/add/", {
            'title': 'Test Album',
            'description': 'Test Description for album',
            'published': 'PUBLIC',
            'photos': [photo.id],
            'cover_photo': ''
        })
        album = Album.public.first()
        self.assertTrue(album.owner == test_user.profile)

    def test_add_album_route_is_status_ok(self):
        """Test that add album view status code is 200."""
        from imager_images.views import AddAlbumView
        test_user = self.add_test_user()
        self.client.force_login(test_user)
        request = self.request.get(reverse_lazy("add_album"))
        request.user = test_user
        view = AddAlbumView.as_view()
        response = view(request)
        self.assertTrue(response.status_code == 200)

    def test_add_album_view_uses_correct_template(self):
        """Test that add album view uses the correct template."""
        test_user = self.add_test_user()
        self.client.force_login(test_user)
        request = self.client.get("/images/albums/add/")
        request.user = test_user
        self.assertTemplateUsed(request, 'imager_images/add_album.html')

    def test_photo_view_is_status_ok(self):
        """Test that photo view status code is 200."""
        photo = self.photos[0]
        test_user = self.add_test_user()
        photo.owner = test_user.profile
        photo.save()
        self.client.force_login(test_user)
        response = self.client.get("/images/photos/" + str(photo.id), follow=True)
        self.assertTrue(response.status_code == 200)

    def test_photo_view_uses_correct_template(self):
        """Test that photo view uses the correct template."""
        photo = self.photos[0]
        test_user = self.add_test_user()
        photo.owner = test_user.profile
        photo.save()
        self.client.force_login(test_user)
        request = self.client.get("/images/photos/" + str(photo.id), follow=True)
        self.assertTemplateUsed(request, 'imager_images/photo.html')

    def test_edit_photo_view_is_status_ok(self):
        """Test that photo view status code is 200."""
        photo = self.photos[0]
        test_user = self.add_test_user()
        photo.owner = test_user.profile
        photo.save()
        self.client.force_login(test_user)
        request = self.client.get("/images/photos/" + str(photo.pk) + "/edit/", follow=True)
        self.assertTrue(request.status_code == 200)

    def test_edit_photo_view_uses_correct_template(self):
        """Test that edit photo view uses the correct template."""
        photo = self.photos[0]
        test_user = self.add_test_user()
        photo.owner = test_user.profile
        photo.save()
        self.client.force_login(test_user)
        request = self.client.get("/images/photos/" + str(photo.id) + "/edit/", follow=True)
        request.user = test_user
        self.assertTemplateUsed(request, 'imager_images/edit_photo.html')

    def test_album_view_is_status_ok(self):
        """Test that album view status code is 200."""
        album = self.albums[0]
        album.published = 'PUBLIC'
        album.save()
        test_user = self.add_test_user()
        self.client.force_login(test_user)
        response = self.client.get("/images/albums/" + str(album.id), follow=True)
        self.assertTrue(response.status_code == 200)

    def test_album_view_is_forbidden_when_not_public_and_not_owned_by_user(self):
        """Test that album view status code is 200."""
        album = self.albums[0]
        album.owner = self.users[0].profile
        album.save()
        test_user = self.add_test_user()
        self.client.force_login(test_user)
        response = self.client.get("/images/albums/" + str(album.id), follow=True)
        self.assertEqual(response.status_code, 403)

    def test_photo_view_is_forbidden_when_not_public_and_not_owned_by_user(self):
        """Test that photo view status code is 200."""
        photo = self.photos[0]
        photo.owner = self.users[0].profile
        photo.save()
        test_user = self.add_test_user()
        self.client.force_login(test_user)
        response = self.client.get("/images/photos/" + str(photo.id), follow=True)
        self.assertEqual(response.status_code, 403)

    def test_album_view_status_ok_when_private_but_owned_by_user(self):
        """Test that album view status code is 200."""
        album = self.albums[0]
        user = self.users[0]
        album.owner = user.profile
        album.save()
        user.save()
        self.client.force_login(user)
        response = self.client.get("/images/albums/" + str(album.id), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_photo_view_status_ok_when_private_but_owned_by_user(self):
        """Test that photo view status code is 200."""
        photo = self.photos[0]
        user = self.users[0]
        photo.owner = user.profile
        photo.save()
        user.save()
        self.client.force_login(user)
        response = self.client.get("/images/photos/" + str(photo.id), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_edit_album_view_is_status_ok(self):
        """Test that album view status code is 200."""
        album = self.albums[0]
        test_user = self.add_test_user()
        album.owner = test_user.profile
        album.save()
        self.client.force_login(test_user)
        response = self.client.get("/images/albums/" + str(album.id) + "/edit", follow=True)
        self.assertTrue(response.status_code == 200)

    def test_edit_album_view_uses_correct_template(self):
        """Test that edit album view status code is 200."""
        album = self.albums[0]
        test_user = self.add_test_user()
        album.owner = test_user.profile
        album.save()
        self.client.force_login(test_user)
        response = self.client.get("/images/albums/" + str(album.id) + "/edit", follow=True)
        self.assertTemplateUsed(response, 'imager_images/edit_album.html')

    # def test_logged_in_user_can_get_to_edit_photo_page(self):
    #     """Test authenticated user can get to edit photo page."""
    #     photo = self.photos[0]
    #     user = self.user_login()
    #     self.client.force_login(user)
    #     response = self.client.get("/images/photos/" + str(photo.pk) + "/edit/")
    #     self.assertTrue(response.status_code == 200)

    def test_home_page_displays_photo(self):
        """Test that there is a photo on the home page."""
        from imagersite.views import HomeView
        photo = Photo.objects.first()
        photo.published = 'PUBLIC'
        photo.title = 'random home photo'
        photo.save()
        request = self.request.get('/')
        view = HomeView.as_view()
        response = view(request)
        soup = Soup(response.rendered_content, 'html.parser')
        photos = soup.find_all('img')
        self.assertEqual(len(photos), 1)

    def test_add_photo_redirects_to_login_if_user_not_logged_in(self):
        """Logged out user should be redirected to login if they try to add a photo."""
        response = self.client.get(reverse_lazy('add_photo'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url[:15], '/accounts/login')

    def test_add_album_redirects_to_login_if_user_not_logged_in(self):
        """Logged out user should be redirected to login if they try to add a album."""
        response = self.client.get(reverse_lazy('add_album'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url[:15], '/accounts/login')

    def test_album_str_method_produces_username(self):
        """Test that the string method for the profile prints the user."""
        album = Album.objects.first()
        self.assertTrue(str(album) == album.title)

    def test_can_add_tags_to_photo(self):
        """Should be able to manually add tags to a photo."""
        photo = self.photos[0]
        photo.tags.add('blue', 'berry', 'pie')
        self.assertCountEqual(['blue', 'berry', 'pie'], [x.slug for x in photo.tags.all()])

    def test_tags_show_up_in_library_view(self):
        """After upload photo, redirected to library page where tags should appear."""
        test_user = self.add_test_user()
        self.client.force_login(test_user)
        response = self.add_photo_to_user(tags='beany babies', follow=True)
        soup = Soup(response.content, 'html.parser')
        tags = soup.find_all('a', class_='tag')
        for tag in tags:
            self.assertTrue(tag.text in ['beany', 'babies'])

    def test_tagged_photo_shows_up_in_tagged_photos_list(self):
        """Photo with tags should show up in the list view for those tags."""
        test_user = self.add_test_user()
        self.client.force_login(test_user)
        self.add_photo_to_user(tags='burpkin, banana')
        self.add_photo_to_user(tags='burpkin, bongos')
        response = self.client.get('/images/photos/tagged/burpkin/')
        soup = Soup(response.content, 'html.parser')
        self.assertEqual(len(soup.find_all('img')), 2)
