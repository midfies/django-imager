
import os
from datetime import datetime

import pytz
from faker import Faker
from bs4 import BeautifulSoup as Soup

from django.urls import reverse
from django.test import TestCase, Client, RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User, AnonymousUser

from imagersite.settings import MEDIA_ROOT
from imager_profile.models import ImagerProfile
from imager_images.models import Photo, Album
from imager_profile.tests import UserFactory, PhotoFactory, AlbumFactory
from imager_images.views import (
    library_view,
    PhotoView,
    AlbumView,
    AlbumGalleryView,
    PhotoGalleryView,
    AddPhotoView,
    AddAlbumView
)
from imagersite.views import HomeView

faker = Faker()


class ImageTestCase(TestCase):
    """Abstract TestCase for images testing."""

    def setUp(self):
        """The appropriate setup for the appropriate test."""
        self.billy = self.add_test_user('BillyTheGoat', 'billyspassword')
        self.bob = UserFactory.create()

        self.request = RequestFactory()
        self.anon_request = RequestFactory()
        self.anon = (AnonymousUser(), {})

        self.client = Client()
        self.anon_client = Client()
        self.client.force_login(self.billy)

        self.photos = [PhotoFactory.create() for i in range(10)]
        self.albums = [AlbumFactory.create() for i in range(10)]
        self.billys_priv_photo, self.billys_priv_album = self.user_photo_album(
            owner=self.billy.profile,
        )
        self.billys_pub_photo, self.billys_pub_album = self.user_photo_album(
            owner=self.billy.profile,
            published='PUBLIC'
        )
        self.bobs_priv_photo, self.bobs_priv_album = self.user_photo_album(
            owner=self.bob.profile,
        )
        self.bobs_pub_photo, self.bobs_pub_album = self.user_photo_album(
            owner=self.bob.profile,
            published='PUBLIC'
        )

    def user_photo_album(self, **kwargs):
        """Create private photo and album."""
        private_photo = PhotoFactory.create(**kwargs)
        private_album = AlbumFactory.create(**kwargs)
        return private_photo, private_album

    def add_test_user(self, username, password):
        """Make test user and return his profile."""
        user = UserFactory.create()
        user.username = username
        user.set_password(password)
        user.save()
        return user

    def tearDown(self):
        """Teardown when tests complete."""
        images_del = os.path.join(MEDIA_ROOT, 'test_*')
        os.system('rm -rf ' + images_del)


class ImageViewsUnitTests(ImageTestCase):
    """Unit test images views."""

    def test_library_route_is_status_ok_logged_in(self):
        """Test that library view status code is 200."""
        request = self.request.get(reverse("library"))
        request.user = self.billy
        response = library_view(request)
        self.assertEqual(response.status_code, 200)

    def test_library_view_redirects_logged_out(self):
        """Test that library view redirects anon user."""
        request = self.anon_request.get(reverse("library"))
        request.user, request.session = self.anon
        response = library_view(request)
        self.assertEqual(response.status_code, 302)

    def test_private_photo_detail_view_is_status_ok_logged_in_owner(self):
        """Test that private photo view allowed for owner."""
        photo = self.billys_priv_photo
        kwargs = {'pk': photo.id}
        request = self.request.get(
            reverse('photo', kwargs=kwargs)
        )
        request.user = self.billy
        view = PhotoView.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_private_photo_detail_view_denied_logged_out(self):
        """Test that private photo view denied for anon user."""
        photo = self.billys_priv_photo
        kwargs = {'pk': photo.id}
        request = self.anon_request.get(
            reverse('photo', kwargs=kwargs)
        )
        request.user, request.session = self.anon
        view = PhotoView.as_view()
        with self.assertRaises(PermissionDenied):
            view(request, **kwargs)

    def test_private_photo_detail_view_denied_non_owner(self):
        """Test that private photo view denied for non-owner."""
        photo = self.bobs_priv_photo
        kwargs = {'pk': photo.id}
        request = self.request.get(
            reverse('photo', kwargs=kwargs)
        )
        request.user = self.billy
        view = PhotoView.as_view()
        with self.assertRaises(PermissionDenied):
            view(request, **kwargs)

    def test_public_photo_detail_view_is_status_ok_logged_out(self):
        """Test that public photo view allowed for anon user."""
        photo = self.billys_pub_photo
        kwargs = {'pk': photo.id}
        request = self.anon_request.get(
            reverse('photo', kwargs=kwargs)
        )
        request.user, request.session = self.anon
        view = PhotoView.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_public_photo_detail_view_is_status_ok_non_owner(self):
        """Test that public photo view allowed for non-owner."""
        photo = self.bobs_pub_photo
        kwargs = {'pk': photo.id}
        request = self.request.get(
            reverse('photo', kwargs=kwargs)
        )
        request.user = self.billy
        view = PhotoView.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_private_album_detail_view_is_status_ok_logged_in_owner(self):
        """Test that private album view allowed for owner."""
        album = self.billys_priv_album
        kwargs = {'pk': album.id}
        request = self.request.get(
            reverse('album', kwargs=kwargs)
        )
        request.user = self.billy
        view = AlbumView.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_private_album_detail_view_denied_logged_out(self):
        """Test that private album view denied for anon user."""
        album = self.billys_priv_album
        kwargs = {'pk': album.id}
        request = self.anon_request.get(
            reverse('album', kwargs=kwargs)
        )
        request.user, request.session = self.anon
        view = AlbumView.as_view()
        with self.assertRaises(PermissionDenied):
            view(request, **kwargs)

    def test_private_album_detail_view_denied_non_owner(self):
        """Test that private album view denied for non-owner."""
        album = self.bobs_priv_album
        kwargs = {'pk': album.id}
        request = self.request.get(
            reverse('album', kwargs=kwargs)
        )
        request.user = self.billy
        view = AlbumView.as_view()
        with self.assertRaises(PermissionDenied):
            view(request, **kwargs)

    def test_public_album_detail_view_is_status_ok_logged_out(self):
        """Test that public album view allowed for anon user."""
        album = self.billys_pub_album
        kwargs = {'pk': album.id}
        request = self.anon_request.get(
            reverse('album', kwargs=kwargs)
        )
        request.user, request.session = self.anon
        view = AlbumView.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_public_album_detail_view_is_status_ok_non_owner(self):
        """Test that public album view allowed for non-owner."""
        album = self.bobs_pub_album
        kwargs = {'pk': album.id}
        request = self.request.get(
            reverse('album', kwargs=kwargs)
        )
        request.user = self.billy
        view = AlbumView.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_photo_gallery_view_is_status_ok_logged_in(self):
        """Test that photo gallery view allowed logged in."""
        request = self.request.get(reverse("photo_gallery"))
        request.user = self.billy
        view = PhotoGalleryView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_photo_gallery_view_is_status_ok_logged_out(self):
        """Test that photo gallery view allowed for anon user."""
        request = self.anon_request.get(reverse("photo_gallery"))
        request.user, request.session = self.anon
        view = PhotoGalleryView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_album_gallery_view_is_status_ok_logged_in(self):
        """Test that photo gallery view allowed logged in."""
        request = self.request.get(reverse("album_gallery"))
        request.user = self.billy
        view = AlbumGalleryView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_album_gallery_view_is_status_ok_logged_out(self):
        """Test that photo gallery view allowed for anon user."""
        request = self.anon_request.get(reverse("album_gallery"))
        request.user, request.session = self.anon
        view = AlbumGalleryView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_add_photo_view_is_status_ok_logged_in(self):
        """Test that add photo view allowed for logged in user."""
        request = self.request.get(reverse("add_photo"))
        request.user = self.billy
        view = AddPhotoView.as_view()
        response = view(request)
        self.assertTrue(response.status_code == 200)

    def test_add_photo_view_is_redirects_logged_out(self):
        """Test that add photo view denies and redirects anon user."""
        request = self.anon_request.get(reverse("add_photo"))
        request.user, request.session = self.anon
        view = AddPhotoView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)

    def test_add_album_view_is_status_ok_logged_in(self):
        """Test that add album view allowed for logged in user."""
        request = self.request.get(reverse("add_album"))
        request.user = self.billy
        view = AddAlbumView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_add_album_view_redirects_logged_out(self):
        """Test that add album view denies and redirects anon user."""
        request = self.request.get(reverse("add_album"))
        request.user, request.session = self.anon
        view = AddAlbumView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)

    def test_add_album_forms_photos_queryset_only_users_photos(self):
        """Assure the available photos to add to album are photos owned by user."""
        request = self.request.get(reverse("add_album"))
        request.user = self.billy
        view = AddAlbumView.as_view()
        response = view(request)
        soup = Soup(response.rendered_content, 'html.parser')
        cover_photo = soup.find('select', attrs={'name': 'cover_photo'})
        cover_options = cover_photo.find_all('option')
        photos = soup.find('select', attrs={'name': 'photos'})
        photo_options = photos.find_all('option')
        billys_photos = self.billy.profile.photos.all()
        self.assertListEqual(
            [p.title for p in billys_photos],
            [tag.text for tag in photo_options]
        )
        self.assertListEqual(
            [p.title for p in billys_photos],
            [tag.text for tag in cover_options[1:]]
        )

    def test_home_page_displays_photo(self):
        """Test that there is a photo on the home page."""
        request = self.request.get('/')
        view = HomeView.as_view()
        response = view(request)
        soup = Soup(response.rendered_content, 'html.parser')
        photos = soup.find_all('img')
        self.assertEqual(len(photos), 1)


class ImageViewsFuncTests(ImageTestCase):
    """The Profile Model test runner for db stuff."""

    def test_private_photo_route_is_status_ok_logged_in_as_owner(self):
        """Test that private photo view allowed for owner."""
        photo = self.billys_priv_photo
        response = self.client.get(
            reverse('photo', kwargs={'pk': photo.id}),
        )
        self.assertEqual(response.status_code, 200)

    def test_private_photo_route_is_status_bad_logged_out(self):
        """Test that private photo view denied for anon user."""
        photo = self.billys_priv_photo
        response = self.anon_client.get(
            reverse('photo', kwargs={'pk': photo.id}),
        )
        self.assertEqual(response.status_code, 403)

    def test_private_photo_route_is_status_bad_non_owner(self):
        """Test that private photo view denied for non-owner."""
        photo = self.bobs_priv_photo
        response = self.client.get(
            reverse('photo', kwargs={'pk': photo.id}),
        )
        self.assertEqual(response.status_code, 403)

    def test_public_photo_route_is_status_ok_logged_out(self):
        """Test that public photo view allowed for anon user."""
        photo = self.billys_pub_photo
        response = self.anon_client.get(
            reverse('photo', kwargs={'pk': photo.id}),
        )
        self.assertEqual(response.status_code, 200)

    def test_public_photo_route_is_status_ok_non_owner(self):
        """Test that public photo view allowed for non-owner."""
        photo = self.bobs_pub_photo
        response = self.client.get(
            reverse('photo', kwargs={'pk': photo.id}),
        )
        self.assertEqual(response.status_code, 200)

    def test_private_album_route_is_status_ok_logged_in_as_owner(self):
        """Test that private album view allowed for owner."""
        album = self.billys_priv_album
        response = self.client.get(
            reverse('album', kwargs={'pk': album.id}),
        )
        self.assertEqual(response.status_code, 200)

    def test_private_album_route_is_status_bad_logged_out(self):
        """Test that private album view denied for anon user."""
        album = self.billys_priv_album
        response = self.anon_client.get(
            reverse('album', kwargs={'pk': album.id}),
        )
        self.assertEqual(response.status_code, 403)

    def test_private_album_route_is_status_bad_non_owner(self):
        """Test that private album view denied for non-owner."""
        album = self.bobs_priv_album
        response = self.client.get(
            reverse('album', kwargs={'pk': album.id})
        )
        self.assertEqual(response.status_code, 403)

    def test_public_album_route_is_status_ok_logged_out(self):
        """Test that public album view allowed for anon user."""
        album = self.billys_pub_album
        response = self.anon_client.get(
            reverse('album', kwargs={'pk': album.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_public_album_route_is_status_ok_non_owner(self):
        """Test that public album view allowed for non-owner."""
        album = self.bobs_pub_album
        response = self.client.get(
            reverse('album', kwargs={'pk': album.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_add_photo_is_status_ok_logged_in(self):
        """Test add photo allowed if user logged in."""
        response = self.client.get(reverse('add_photo'))
        self.assertEqual(response.status_code, 200)

    def test_add_photo_redirects_logged_out(self):
        """Test add photo denied if user logged out."""
        response = self.anon_client.get(reverse('add_photo'), follow=True)
        self.assertListEqual(
            response.redirect_chain,
            [('/accounts/login/?next=' + reverse('add_photo'), 302)]
        )

    def test_add_album_is_status_ok_logged_in(self):
        """Test add album allowed if user logged in."""
        response = self.client.get(reverse('add_album'))
        self.assertEqual(response.status_code, 200)

    def test_add_album_redirects_logged_out(self):
        """Test add album denied if user logged out."""
        response = self.anon_client.get(reverse('add_album'), follow=True)
        self.assertListEqual(
            response.redirect_chain,
            [('/accounts/login/?next=' + reverse('add_album'), 302)]
        )

    def test_edit_photo_route_is_status_ok_for_owner(self):
        """Test that edit photo view status code is 200."""
        photo = self.billys_priv_photo
        response = self.client.get(
            reverse('edit_photo', kwargs={'pk': photo.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_edit_private_photo_route_denies_logged_out(self):
        """Test that edit photo view status code is 200."""
        photo = self.billys_priv_photo
        response = self.anon_client.get(
            reverse('edit_photo', kwargs={'pk': photo.id})
        )
        self.assertEqual(response.status_code, 403)

    def test_edit_private_photo_route_denies_non_owner(self):
        """Test that edit photo view status code is 200."""
        photo = self.bobs_priv_photo
        response = self.client.get(
            reverse('edit_photo', kwargs={'pk': photo.id})
        )
        self.assertEqual(response.status_code, 403)

    def test_edit_public_photo_route_denies_logged_out(self):
        """Test that edit photo view status code is 200."""
        photo = self.bobs_pub_photo
        response = self.anon_client.get(
            reverse('edit_photo', kwargs={'pk': photo.id})
        )
        self.assertEqual(response.status_code, 403)

    def test_edit_public_photo_route_denies_non_owner(self):
        """Test that edit photo view status code is 200."""
        photo = self.bobs_pub_photo
        response = self.client.get(
            reverse('edit_photo', kwargs={'pk': photo.id})
        )
        self.assertEqual(response.status_code, 403)

    def test_edit_album_route_is_status_ok_for_owner(self):
        """Test that edit album view allowed for owner."""
        album = self.billys_priv_album
        response = self.client.get(
            reverse('edit_album', kwargs={'pk': album.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_edit_private_album_route_denies_logged_out(self):
        """Test that edit private album view denies anon user."""
        album = self.billys_priv_album
        response = self.anon_client.get(
            reverse('edit_album', kwargs={'pk': album.id})
        )
        self.assertEqual(response.status_code, 403)

    def test_edit_private_album_route_denies_non_owner(self):
        """Test that edit private album view denies logged out."""
        album = self.bobs_priv_album
        response = self.client.get(
            reverse('edit_album', kwargs={'pk': album.id})
        )
        self.assertEqual(response.status_code, 403)

    def test_edit_public_album_route_denies_logged_out(self):
        """Test that edit public album view denies anon user."""
        album = self.bobs_pub_album
        response = self.anon_client.get(
            reverse('edit_album', kwargs={'pk': album.id})
        )
        self.assertEqual(response.status_code, 403)

    def test_edit_public_album_route_denies_non_owner(self):
        """Test that edit public album view denies non-owner."""
        album = self.bobs_pub_album
        response = self.client.get(
            reverse('edit_album', kwargs={'pk': album.id})
        )
        self.assertEqual(response.status_code, 403)

    def test_photo_route_uses_correct_template(self):
        """Test that photo view uses the correct template."""
        photo = self.billys_priv_photo
        response = self.client.get(
            reverse('photo', kwargs={'pk': photo.id})
        )
        self.assertTemplateUsed(response, 'imager_images/photo.html')

    def test_album_route_uses_correct_template(self):
        """Test that album view uses the correct template."""
        album = self.billys_priv_album
        response = self.client.get(
            reverse('album', kwargs={'pk': album.id})
        )
        self.assertTemplateUsed(response, 'imager_images/album.html')

    def test_library_route_uses_correct_template(self):
        """Test that library view uses the correct template."""
        response = self.client.get(reverse('library'))
        self.assertTemplateUsed(response, 'imager_images/library.html')

    def test_photo_gallery_uses_correct_template(self):
        """Test that photo gallery view uses the correct template."""
        response = self.client.get(reverse('photo_gallery'))
        self.assertTemplateUsed(response, 'imager_images/photo_gallery.html')

    def test_album_gallery_uses_correct_template(self):
        """Test that album gallery view uses the correct template."""
        response = self.client.get(reverse('album_gallery'))
        self.assertTemplateUsed(response, 'imager_images/album_gallery.html')

    def test_add_photo_route_uses_correct_template(self):
        """Test that add photo view uses the correct template."""
        response = self.client.get(reverse('add_photo'))
        self.assertTemplateUsed(response, 'imager_images/add_photo.html')

    def test_add_album_route_uses_correct_template(self):
        """Test that add album view uses the correct template."""
        response = self.client.get(reverse('add_album'))
        self.assertTemplateUsed(response, 'imager_images/add_album.html')

    def test_edit_photo_route_uses_correct_template(self):
        """Test that edit photo view uses the correct template."""
        photo = self.billys_priv_photo
        response = self.client.get(
            reverse('edit_photo', kwargs={'pk': photo.id}),
            follow=True
        )
        self.assertTemplateUsed(response, 'imager_images/edit_photo.html')

    def test_edit_album_route_uses_correct_template(self):
        """Test that edit album view uses the correct template."""
        album = self.billys_priv_album
        response = self.client.get(
            reverse('edit_album', kwargs={'pk': album.id}),
            follow=True
        )
        self.assertTemplateUsed(response, 'imager_images/edit_album.html')

    def post_to_billy(self, route, data, follow=False):
        """Post data to form as billy."""
        get = self.client.get(reverse(route))
        data = data.copy()
        data['csrftoken'] = get.cookies['csrftoken'].value
        post = self.client.post(
            reverse(route),
            data,
            follow=follow
        )
        return post

    def post_photo_to_billy(self, **kwargs):
        """Post request to add_photo."""
        data = {
            'title': 'DefaultTitle',
            'description': 'DefaultDescription',
            'photo': SimpleUploadedFile(
                'test.jpg',
                open('imager_images/static/generic.jpg', 'rb').read()),
            'published': 'PRIVATE',
            'tags': '',
        }
        data.update(kwargs)
        return self.post_to_billy('add_photo', data, follow=True)

    def post_album_to_billy(self, ids, cover_photo_id, **kwargs):
        """Post request to add_album."""
        data = {
            'title': 'DefaultAlbumTitle',
            'description': 'DefaultAlbumDescription',
            'photos': ids,
            'cover_photo': cover_photo_id,
            'published': 'PRIVATE',
        }
        data.update(kwargs)
        return self.post_to_billy('add_album', data, follow=True)

    def test_add_photo_adds_models_and_sets_fields(self):
        """Test that post to add_photo adds photo and attaches owner."""
        count_before = Photo.objects.count()
        data = {
            'title': 'soidjicds',
            'description': 'asdfjojic',
            'published': 'PUBLIC'
        }
        self.post_photo_to_billy(**data)
        photo = Photo.objects.last()
        self.assertEqual(Photo.objects.count(), count_before + 1)
        for field, value in data.items():
            self.assertEqual(getattr(photo, field), value)

    def test_add_photo_route_relates_owner(self):
        """Test that post to add_photo relates photo to owner."""
        self.post_photo_to_billy(title='billyshouldownthis')
        photo = Photo.objects.get(title='billyshouldownthis')
        self.assertEqual(photo.owner, self.billy.profile)
        self.assertEqual(self.billy.profile.photos.last(), photo)

    def test_add_photo_route_adds_tags(self):
        """Test that post to add_photo adds tags to photo."""
        tags = faker.words(5)
        self.post_photo_to_billy(
            title='photowithtags',
            tags=','.join(tags)
        )
        photo = Photo.objects.get(title='photowithtags')
        self.assertListEqual(
            sorted([t.name for t in photo.tags.all()]),
            sorted(tags)
        )

    def test_add_album_adds_models_and_sets_fields(self):
        """Test that post to add_album adds album and attaches owner."""
        billys_photos = self.billy.profile.photos.all()
        ids = [p.id for p in billys_photos]
        count_before = Album.objects.count()
        data = {
            'title': 'cdsicjiosd',
            'description': 'gobbledeegook',
            'published': 'PUBLIC'
        }
        self.post_album_to_billy(ids, ids[0], **data)
        album = Album.objects.last()
        self.assertEqual(Album.objects.count(), count_before + 1)
        for field, value in data.items():
            self.assertEqual(getattr(album, field), value)
        self.assertListEqual(
            list(album.photos.all()),
            list(billys_photos)
        )

    def test_add_album_route_relates_owner(self):
        """Test that post to add_photo relates album to owner."""
        billys_photos = self.billy.profile.photos.all()
        ids = [p.id for p in billys_photos]
        self.post_album_to_billy(ids[:1], ids[0])
        album = Album.objects.last()
        self.assertEqual(album.owner, self.billy.profile)
        self.assertEqual(self.billy.profile.albums.last(), album)

    def test_tags_show_up_in_library_view(self):
        """After upload photo, redirected to library page where tags should appear."""
        tag_set = set()
        tagss = ['random', 'bongos,random,boredom', 'billybob,thornguy']
        for tags in tagss:
            tag_set.update(tags.split(','))
            self.post_photo_to_billy(tags=tags)
        response = self.client.get(reverse('library') + '?photos_per_page=20')
        soup = Soup(response.content, 'html.parser')
        soup_tags = set([t.text for t in soup.find_all('a', class_='tag')])
        for tag in tag_set:
            self.assertIn(tag, soup_tags)

    def test_tagged_photo_shows_up_in_tagged_photos_list(self):
        """Photo with tags should show up in the list view for those tags."""
        tagss = ['burpkin,banana', 'bongos,burpkin', 'billybob,thornguy']
        for tags in tagss:
            self.post_photo_to_billy(tags=tags)
        response = self.client.get(reverse('tagged_photos', kwargs={'slug': 'burpkin'}))
        soup = Soup(response.content, 'html.parser')
        self.assertEqual(len(soup.find_all('img')), 2)


class PhotoModelTests(TestCase):
    """Unit test photo fields, relations, db queries."""

    def add_photo(self, **kwargs):
        """Add photo to db."""
        photo = PhotoFactory.create()
        for kwarg in kwargs:
            setattr(photo, kwarg, kwargs[kwarg])
        photo.save()

    def test_can_add_photo(self):
        """Assure a photo can be added and retrieved."""
        count_before = Photo.objects.count()
        self.add_photo(title='notuniq')
        self.assertEqual(Photo.objects.count() - count_before, 1)

    def test_last_photo_is_last_added(self):
        """Test last photo added is same when retrieved by title or by last."""
        self.add_photo(title='lastadded')
        self.assertEqual(
            Photo.objects.get(title='lastadded'),
            Photo.objects.last()
        )

    def test_can_add_photo_with_fields(self):
        """Assure photos can be added and retrieved with fields attached."""
        fields = {
            'title': 'superunique',
            'description': 'longdescription',
            'published': 'PUBLIC',
        }
        self.add_photo(date_published=datetime.now(tz=pytz.utc), **fields)
        photo = Photo.objects.last()
        self.assertIsInstance(photo.date_published, datetime)
        for field in fields:
            self.assertEqual(getattr(photo, field), fields[field])

    def test_photos_default_fields(self):
        """Test photo models default fields are valid."""
        self.add_photo()
        photo = Photo.objects.last()
        self.assertEqual(photo.published, 'PRIVATE')
        self.assertIsInstance(photo.date_modified, datetime)
        self.assertIsInstance(photo.date_uploaded, datetime)

    def test_can_add_tags_to_photo(self):
        """Should be able to manually add tags to a photo."""
        self.add_photo()
        photo = Photo.objects.last()
        photo.tags.add('blue', 'berry', 'pie')
        photo.save()
        dbphoto = Photo.objects.last()
        self.assertCountEqual(
            ['blue', 'berry', 'pie'],
            [x.slug for x in dbphoto.tags.all()]
        )

    def test_photos_ordered_by_date(self):
        """Test photos are ordered by date uploaded."""
        for i in range(10):
            photo = PhotoFactory()
            photo.save()
        dbphotos = Photo.objects.all()
        self.assertEqual(
            list(dbphotos),
            list(dbphotos.order_by('date_published'))
        )

    def test_public_photo_model_manager(self):
        """Test public model manager returns all, and only, public photos."""
        self.assertListEqual(
            list(Photo.objects.filter(published='PUBLIC')),
            list(Photo.public.all())
        )


class AlbumModelTests(TestCase):
    """Test album model."""

    def setUp(self):
        """Add some photos."""
        self.photos = [PhotoFactory.create() for i in range(10)]

    def add_album(self, **kwargs):
        """Add album to db."""
        album = AlbumFactory.create()
        for kwarg in kwargs:
            setattr(album, kwarg, kwargs[kwarg])
        album.save()

    def test_can_add_album(self):
        """Assure a album can be added and retrieved."""
        count_before = Album.objects.count()
        self.add_album(title='notuniq')
        self.assertEqual(Album.objects.count() - count_before, 1)

    def test_last_album_is_last_added(self):
        """Test last album added is same when retrieved by title or by last."""
        self.add_album(title='lastadded')
        self.assertEqual(
            Album.objects.get(title='lastadded'),
            Album.objects.last()
        )

    def test_can_add_album_with_fields(self):
        """Assure albums can be added and retrieved with fields attached."""
        fields = {
            'title': 'superunique',
            'description': 'longdescription',
            'published': 'PUBLIC',
        }
        self.add_album(date_published=datetime.now(tz=pytz.utc), **fields)
        album = Album.objects.last()
        self.assertIsInstance(album.date_published, datetime)
        for field in fields:
            self.assertEqual(getattr(album, field), fields[field])

    def test_albums_default_fields(self):
        """Test album models default fields are valid."""
        self.add_album()
        album = Album.objects.last()
        self.assertEqual(album.published, 'PRIVATE')
        self.assertIsInstance(album.date_modified, datetime)
        self.assertIsInstance(album.date_uploaded, datetime)

    def test_albums_ordered_by_date(self):
        """Test albums are ordered by date uploaded."""
        for i in range(10):
            albums = AlbumFactory()
            albums.save()
        dbalbums = Album.objects.all()
        self.assertEqual(
            list(dbalbums),
            list(dbalbums.order_by('date_published'))
        )

    def test_can_add_photos_to_album(self):
        """Photo can be associated with albums."""
        album = AlbumFactory()
        for photo in self.photos:
            album.photos.add(photo)
        album.save()
        self.assertListEqual(
            list(album.photos.all()),
            list(self.photos)
        )

    def test_public_album_model_manager(self):
        """Test public model manager returns all, and only, public albums."""
        self.assertListEqual(
            list(Album.objects.filter(published='PUBLIC')),
            list(Album.public.all())
        )


class TearDownTest(TestCase):
    """Teardown."""

    def test_teardown(self):
        """Teardown when tests complete."""
        test_images = os.path.join(MEDIA_ROOT, 'test_*')
        os.system('rm -rf ' + test_images)
        self.assertFalse(any(file.startswith('test_') for file in os.listdir(MEDIA_ROOT)))
