"""Views for albums and photos."""
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from imager_profile.models import ImagerProfile
from imager_images.models import Album, Photo
from imager_images.forms import (AddAlbumForm,
                                 AddPhotoForm,
                                 EditPhotoForm,
                                 EditAlbumForm)

# Create your views here.


class LibraryView(ListView):
    """"LibraryView."""

    template_name = 'imager_images/library.html'

    def get_context_data(self):
        """Get albums and photos and return them."""
        profile = ImagerProfile.active.get(user__username=self.request.user.username)
        photos = profile.photos.all()
        albums = profile.albums.all()
        username = self.request.user.username
        return {'photos': photos,
                'profile': profile,
                'albums': albums,
                'username': username}

    def get_queryset(self):
        """Redefining because I have to."""
        return {}


class AlbumView(UserPassesTestMixin, ListView):
    """"AlbumView."""

    template_name = 'imager_images/album.html'
    model = Album
    raise_exception = True
    permission_denied_message = "You don't have access to this album."

    def test_func(self):
        """Override the userpassestest test_func."""
        album = get_object_or_404(Album, id=self.kwargs['albumid'])
        return album.published == 'PUBLIC' or album.owner.user == self.request.user

    def get_context_data(self):
        """Get albums and photos and return them."""
        album = Album.objects.get(id=self.kwargs['albumid'])
        photos = album.photos.all()
        return {'album': album, 'photos': photos}


class PhotoView(UserPassesTestMixin, DetailView):
    """"AlbumView."""

    template_name = 'imager_images/photo.html'
    model = Photo
    raise_exception = True
    permission_denied_message = "You don't have access to this photo."

    def test_func(self):
        """Override the userpassestest test_func."""
        photo = get_object_or_404(Photo, id=self.kwargs['pk'])
        return photo.published == 'PUBLIC' or photo.owner.user == self.request.user


class AlbumGalleryView(ListView):
    """"AlbumGalleryView."""

    template_name = 'imager_images/album_gallery.html'

    def get_context_data(self):
        """Get all public albums return them."""
        albums = Album.public.all()
        return {'albums': albums}

    def get_queryset(self):
        """Redefining because I have to."""
        return {}


class PhotoGalleryView(ListView):
    """"PhotoGalleryView."""

    template_name = 'imager_images/photo_gallery.html'

    def get_context_data(self):
        """Get all public photos and return them."""
        photos = Photo.public.all()
        return {'photos': photos}

    def get_queryset(self):
        """Redefining because I have to."""
        return {}


class AddAlbumView(LoginRequiredMixin, CreateView):
    """Add a new album."""

    login_required = True
    success_url = reverse_lazy('library')
    template_name = 'imager_images/add_album.html'
    model = Album
    form_class = AddAlbumForm

    def get_form(self):
        """Retrieve form and customize some fields."""
        form = super(AddAlbumView, self).get_form()
        form.fields['cover_photo'].queryset = self.request.user.profile.photos.all()
        form.fields['photos'].queryset = self.request.user.profile.photos.all()
        # import pdb; pdb.set_trace()
        return form

    def form_valid(self, form):
        """If form post is successful, set the object's owner."""
        # import pdb; pdb.set_trace()
        self.object = form.save()
        self.object.owner = self.request.user.profile
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class EditAlbumView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edit an album."""

    login_required = True
    success_url = reverse_lazy('library')
    template_name = 'imager_images/edit_album.html'
    model = Album
    form_class = EditAlbumForm
    raise_exception = True
    permission_denied_message = "You don't have access to this album."

    def test_func(self):
        """Override the userpassestest test_func."""
        album = self.get_object()
        return album.owner.user == self.request.user

    def get_form(self):
        """Retrieve form and customize some fields."""
        form = super(EditAlbumView, self).get_form()
        form.fields['cover_photo'].queryset = self.request.user.profile.photos.all()
        form.fields['photos'].queryset = self.request.user.profile.photos.all()
        return form


class AddPhotoView(LoginRequiredMixin, CreateView):
    """Add a new photo."""

    login_required = True
    success_url = reverse_lazy('library')
    template_name = 'imager_images/add_photo.html'
    model = Photo
    form_class = AddPhotoForm

    def form_valid(self, form):
        """If form post is successful, set the object's owner."""
        self.object = form.save()
        self.object.owner = self.request.user.profile
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class EditPhotoView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edit a photo."""

    login_required = True
    success_url = reverse_lazy('library')
    template_name = 'imager_images/edit_photo.html'
    model = Photo
    form_class = EditPhotoForm
    form_class.Meta.exclude.append('photo')
    raise_exception = True
    permission_denied_message = "You don't have access to this album."

    def test_func(self):
        """Override the userpassestest test_func."""
        photo = self.get_object()
        return photo.owner.user == self.request.user
