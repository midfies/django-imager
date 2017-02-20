"""Views for albums and photos."""
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from imager_profile.models import ImagerProfile
from imager_images.models import Album, Photo
from imager_images.forms import (AddAlbumForm,
                                 AddPhotoForm,
                                 EditPhotoForm,
                                 EditAlbumForm)


@login_required
def LibraryView(request):
    """List view of user's albums and photos."""
    profile = get_object_or_404(ImagerProfile.active, user__username=request.user.username)
    all_albums = profile.albums.all()
    all_photos = profile.photos.all()
    album_page = request.GET.get("album_page", 1)
    photo_page = request.GET.get("photo_page", 1)

    album_pages = Paginator(all_albums, 4)
    photo_pages = Paginator(all_photos, 4)

    try:
        albums = album_pages.page(album_page)
        photos = photo_pages.page(photo_page)
    except PageNotAnInteger:
        albums = album_pages.page(1)
        photos = photo_pages.page(1)
    except EmptyPage:
        albums = album_pages.page(album_pages.num_pages)
        photos = photo_pages.page(photo_pages.num_pages)

    return render(request,
                  "imager_images/library.html",
                  {"albums": albums, 'photos': photos})


class AlbumView(UserPassesTestMixin, ListView):
    """"AlbumView."""

    template_name = 'imager_images/album.html'
    model = Album
    raise_exception = True
    paginate_by = 4
    permission_denied_message = "You don't have access to this album."

    def test_func(self):
        """Override the userpassestest test_func."""
        self.album = get_object_or_404(Album, id=self.kwargs['albumid'])
        return self.album.published == 'PUBLIC' or self.album.owner.user == self.request.user

    def get_context_data(self, **kwargs):
        """Get albums and photos and return them."""
        context = super(AlbumView, self).get_context_data(**kwargs)
        context['album'] = self.album
        return context

    def get_queryset(self):
        """Return photos assoicated with album."""
        return self.album.photos.all()


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

    def get_context_data(self, **kwargs):
        """Include like-tagged photos."""
        context = super(PhotoView, self).get_context_data(**kwargs)
        context['tag_photos'] = context['photo'].tags.similar_objects()[:5]
        return context


class AlbumGalleryView(ListView):
    """"AlbumGalleryView."""

    template_name = 'imager_images/album_gallery.html'
    context_object_name = 'albums'
    paginate_by = 4
    queryset = Album.public.all()


class PhotoGalleryView(ListView):
    """"PhotoGalleryView."""

    template_name = 'imager_images/photo_gallery.html'
    context_object_name = 'photos'
    queryset = Photo.public.all()


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


class TagPhotoGalleryView(ListView):
    """List photos with a tag."""

    template_name = 'imager_images/photo_gallery.html'
    context_object_name = 'photos'

    def get_queryset(self):
        """Define a restricted queryset just for certain tag."""
        return Photo.public.filter(tags__slug=self.kwargs.get("slug")).all()

    def get_context_data(self, **kwargs):
        """Get context."""
        context = super(TagPhotoGalleryView, self).get_context_data(**kwargs)
        context["tag"] = self.kwargs.get("slug")
        return context
