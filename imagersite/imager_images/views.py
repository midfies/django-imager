"""Views for albums and photos."""
from django.views.generic.edit import CreateView
from django.views.generic import ListView, TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden

from imager_profile.models import ImagerProfile
from imager_images.models import Album, Photo
from imager_images.forms import AddAlbumForm, AddPhotoForm

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
        return {'photos': photos, 'profile': profile, 'albums': albums, 'username': username}

    def get_queryset(self):
        """Redefining because I have to."""
        return {}


class AlbumView(ListView):
    """"AlbumView."""

    template_name = 'imager_images/album.html'
    model = Album

    def get_context_data(self):
        """Get albums and photos and return them."""
        album = Album.objects.get(id=self.kwargs['albumid'])
        if album.published == 'PUBLIC' or album.owner == self.request.user.profile:
            photos = album.photos.all()
            return {'album': album, 'photos': photos}
        else:
            return HttpResponseForbidden()


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


class AddAlbumView(CreateView):
    """Add a new album."""
    login_required = True
    success_url = reverse_lazy('library')
    template_name = 'imager_images/add_album.html'
    model = Album
    fields = [
        'title',
        'description',
        'published',
        'cover_photo',
        'photos'
    ]

    def form_valid(self, form):
        self.object = form.save()
        import pdb; pdb.set_trace()
        self.object.owner = self.request.user.profile
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class AddPhotoView(CreateView):
    """Add a new photo."""
    login_required = True
    success_url = reverse_lazy('library')
    template_name = 'imager_images/add_photo.html'
    model = Photo
    fields = [
        'title',
        'description',
        'published',
        'photo'
    ]

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user.profile
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
